#!/usr/bin/env python3
"""不変ルール7の git 検出: 実施済み（学び LEARN が紐づいた）ACT の行動計画（テストカード）が
base と比べて書き換えられていないかをチェックする（pre-commit は --staged、レビュー時は --base <ref>）。

ACT（行動計画）と LEARN（実施後の学び）はレコードとして分離されている。ある ACT に learns-from で
紐づく LEARN が base 時点で既に存在していれば、その試行は検証開始済み＝行動計画は凍結する
（成功基準を後知恵で書き換えない）。まだ学びが無い ACT は行動計画を直してよい（事後補完も可）。
"""
import argparse
import re
import subprocess
import sys

PLAN_RE = re.compile(r"## 行動計画.*\Z", re.DOTALL)
ACT_ID_RE = re.compile(r"([A-Z0-9]+-ACT-\d+)")


def git(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False)


def testcard(text: str) -> str:
    m = PLAN_RE.search(text)
    return m.group(0) if m else text


def parse_learns_from(text: str) -> list:
    """LEARN frontmatter の learns-from（単一 or 配列表記）から ACT id を取り出す。"""
    m = re.search(r"^learns-from:\s*(.*)$", text, re.MULTILINE)
    if not m:
        return []
    return ACT_ID_RE.findall(m.group(1))


def executed_acts_at(ref: str) -> set:
    """ref 時点で LEARN（learns-from）が紐づいている ACT id の集合。"""
    out = set()
    tree = git("ls-tree", "-r", "--name-only", ref)
    if tree.returncode != 0:
        return out
    for f in tree.stdout.splitlines():
        if "/wiki/learnings/" not in f or not f.endswith(".md"):
            continue
        show = git("show", f"{ref}:{f}")
        if show.returncode == 0:
            out.update(parse_learns_from(show.stdout))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="HEAD", help="比較先の git ref（既定 HEAD）")
    ap.add_argument("--staged", action="store_true",
                    help="pre-commit モード: base とステージ済み内容（index）を比較する")
    args = ap.parse_args()
    if args.staged:
        diff = git("diff", "--cached", "--name-only", args.base)
    else:
        diff = git("diff", "--name-only", f"{args.base}...HEAD")
    changed = [f for f in diff.stdout.splitlines()
               if "/wiki/activities/" in f and f.endswith(".md")]
    executed = executed_acts_at(args.base)   # base 時点で学びが紐づいていた ACT
    failures = []
    for f in changed:
        act_id_match = ACT_ID_RE.search(f)
        if not act_id_match or act_id_match.group(1) not in executed:
            continue  # 学びがまだ無い（検証開始前）の行動計画は直してよい
        base_show = git("show", f"{args.base}:{f}")
        if base_show.returncode != 0:
            continue  # 新規ファイルは対象外
        if args.staged:
            head_show = git("show", f":{f}")
            if head_show.returncode != 0:
                continue  # 削除は対象外
            head_text = head_show.stdout
        else:
            try:
                head_text = open(f, encoding="utf-8").read()
            except FileNotFoundError:
                continue  # 削除されたファイルは対象外
        if testcard(base_show.stdout) != testcard(head_text):
            failures.append(f)
    for f in failures:
        print(f"[error] testcard-immutable | {f} | "
              "学び(LEARN)が紐づいた実施済みACTの行動計画（成功基準）が変更されている"
              "（不変ルール7・後知恵バイアス防止）")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
