# projects/ — 個人案件（人単位）

目的形成は**案件（人）単位**で分ける。各案件は自分の生データ（`sources/`）と Wiki（`wiki/`）を1フォルダに持つ。スキーマ層（`ontology.yaml`・`CLAUDE.md`・`AGENTS.md`・`playbooks/`・`templates/`・`.claude/skills/`）はリポジトリ全体で共有する。

現在アクティブな案件は各自ローカルの `.env` の `CURRENT_PROJECT=<slug>`（未設定なら `self`）が指す（`.env` は gitignore・書式はリポ直下の `.env.example`）。案件の一覧ファイルは持たない——slug はこのディレクトリ名、接頭辞（PREFIX）は各案件の既存レコードID（無ければ `slug` の大文字）から導出する。

```
projects/
├── <slug>/
│   ├── sources/          # この案件の生データ（不変層・AIは読むだけ・冒頭に種別タグ）
│   └── wiki/
│       ├── purposes/<PREFIX>-P-NNN.md       # 目的仮説
│       ├── constraints/<PREFIX>-C-NNN.md     # 制約・手中の鳥
│       ├── activities/<PREFIX>-ACT-NNN.md    # 試行
│       ├── reflections/<PREFIX>-REF-NNN.md   # 内省
│       ├── decisions/<PREFIX>-DEC-NNN.md     # 意思決定
│       ├── views/         # 生成物
│       ├── index.md ├── log.md ├── stage.md └── explore-log.md
└── ...
```

## ID は接頭辞つき（Obsidian のリンク一意性のため）

- ファイル名＝ID で、**案件接頭辞つき**（例 `SELF-P-001.md`）。infix は P/C/ACT/LEARN/REF/DEC。
- 採番は**種別×案件ごと**の既存最大+1。ID再利用禁止（取り下げた番号は欠番）。

## 新しい案件の作り方

**推奨: `/new-person` スキル**を使う。`templates/project/` の雛形から `projects/<slug>/` を作り、`.env` の `CURRENT_PROJECT` を切り替えるところまで行う。

手動で作る場合:

1. `cp -r templates/project/. projects/<slug>/`（`sources/` と空の `wiki/` 一式が揃う）。
2. `wiki/stage.md`・`explore-log.md`・`log.md` の `YYYY-MM-DD` を今日の日付にする。
3. 接頭辞（大文字・他案件のレコードID接頭辞と重複しない。既定は `slug` の大文字）を決める。切り替えは `.env` に `CURRENT_PROJECT=<slug>` を書く（無ければ作成）。

## 現在の案件

- 切り替えは `.env` の `CURRENT_PROJECT`（未設定なら `self`）。ドッグフーディングは `self`／接頭辞 `SELF`。
