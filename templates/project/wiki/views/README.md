# views/ — 生成物（手編集禁止）

このディレクトリのファイルは `tools/gen_views.py` がレコード（SSoT）から決定論射影する**再生成可能な生成物**である。Claude Code では Stop フック（`tools/hooks/stop_view_gen.py`）がレコード変更時に自動再生成するので、**見たいときはこのフォルダのファイルをそのまま読めばよい**。

- **手で編集しない。** 記録の修正は目的・制約・試行・学び・意思決定の各レコード側で行い、ビューは再生成する。矛盾したら**レコードが正**。
- `purposes-list.md`（`list`） — 目的仮説テーブル＋**目的の系譜**図（`leads-to`/`derived-from`/`revises`、★=`core`）＋次に確かめるべき目的。系譜や ★ を出したいときはビューでなくレコード側の frontmatter に書く。
- `board.md`（`board`） — 試行（ACT）を1実験として時系列に並べる試行ボード（`riskiest-assumption`・行動計画・紐づく LEARN の学びの要点と `outcome`）＋現在地。
- `relations.md`（`relations`） — 全関係型のグラフ＋関係インデックス＋バックリンク索引＋目的↔制約の接地（`grounded-in`）フィット。

ターンの途中でレコードを変更した直後など、その場で作り直したいときだけ手動で再生成する（フックはターン終了時に走るため、ターン中のビューは古いことがある）:

```bash
python3 tools/gen_views.py list|board|relations   # 現在案件（--project <slug> で指定可）
```

Obsidianのグラフビューを使うときは、このフォルダをフィルタで除外すると目的ネットワークが見やすい。
