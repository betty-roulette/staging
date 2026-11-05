# べちぱーCup Vol.1 Staging 初回制作結果

作業日：2026年11月5日（日本時間）

通常7ページとPG-001をローカルで制作・ビルドした。Commit・Push・公開・GitHub Pages設定変更は実施していない。

## ページと生成先

URLの共通接頭辞は `https://betty-roulette.github.io/staging/`。以下のURL欄はその後ろのパスを示す。これは生成先の対応であり、リモートへの公開確認を意味しない。

| PG | ページ | ソース | 生成先 | URL末尾 |
| --- | --- | --- | --- | --- |
| PG-001 | トップページ | src/pages/index.astro | docs/index.html | （接頭辞そのもの） |
| PG-002 | べちぱーCup Vol.1 | src/pages/betipercup/index.astro | docs/betipercup/index.html | betipercup/ |
| PG-004 | 大会概要 | src/pages/betipercup/overview/index.astro | docs/betipercup/overview/index.html | betipercup/overview/ |
| PG-005 | 大会ルール概要・詳細 | src/pages/betipercup/rules/index.astro | docs/betipercup/rules/index.html | betipercup/rules/ |
| PG-006 | 大会ルール詳細 | src/pages/betipercup/rules/detail/index.astro | docs/betipercup/rules/detail/index.html | betipercup/rules/detail/ |
| PG-007 | サバイバー：ルール | src/pages/betipercup/rules/survivor/index.astro | docs/betipercup/rules/survivor/index.html | betipercup/rules/survivor/ |
| PG-008 | キラー：ルール | src/pages/betipercup/rules/killer/index.astro | docs/betipercup/rules/killer/index.html | betipercup/rules/killer/ |
| PG-009 | スケジュール：全体 | src/pages/betipercup/schedule/index.astro | docs/betipercup/schedule/index.html | betipercup/schedule/ |

PG-003、404、その他の対象外ページは制作していない。

## 新規作成・変更ファイル

変更（作業開始時点から存在したファイル）：

- `.gitignore`：作業用の `/tmp/` を除外。
- `package.json`：buildを画像保護用の `node scripts/build.mjs` へ変更。依存パッケージは変更していない。
- `src/pages/index.astro`：初期テンプレートを0秒meta refreshのPG-001へ変更。
- `docs/index.html`：ビルドによりPG-001として再生成。

新規ソース・共通部品：

- `src/components/Head.astro`
- `src/components/Header.astro`
- `src/components/Menu.astro`
- `src/components/Footer.astro`
- `src/components/ReferencedImage.astro`
- `src/components/ImageCard.astro`
- `src/components/Info.astro`
- `src/components/ParentLink.astro`
- `src/layouts/Page.astro`
- `src/lib/site.ts`
- `src/styles/site.css`
- 上表の通常7ページの `.astro` ファイル。
- `public/.nojekyll`（空ファイル）
- `scripts/build.mjs`
- `scripts/verify-build.py`
- `IMPLEMENTATION-REPORT.md`（本報告）

新規生成物：

- 上表の通常7ページのHTML。
- `docs/.nojekyll`（空ファイル）
- `docs/_astro/Info.CyGXKFQ3.css`

作業用ファイルは `tmp/` に格納し、Commit候補から除外する。PDFから抽出した文字、台帳のセル値、レイアウト検証スクリプト・結果等を含む。公開フォルダーには配置していない。

## ビルド・検証結果

- `npm run build`：成功、8ページ生成、終了コード0。
- 実行環境のPATHにnpmがなかったため、`C:/Program Files/nodejs/npm.cmd run build` で同じnpmスクリプトを実行した。
- `public/.nojekyll`・`docs/.nojekyll` はともに0バイト。
- 生成HTMLは対象8件だけ。URL・ディレクトリの対応、内部相対リンクを検証した。
- 全8件で `lang="ja"`、viewport、`<meta name="robots" content="noindex">`、favicon参照3件を検証した。
- 全8件でOGPメタデータがないことを確認した。
- PG-001は `content="0;url=./betipercup/"`。共通ヘッダー・フッターなし。
- 通常ページの共通部品、カード件数、表の件数、PG-009のリンク無効状態を検証した。
- PDF本文と生成HTMLの段落・箇条書き・表セル128箇所を、抽出由来の空白を除いて照合した。
- 画像リクエストをすべて遮断したヘッドレスブラウザーで、7ページ×9幅＝63ケースを確認した。幅は390・414・844・896・960・961・1024・1440・1920px。本文幅、グリッド列数、表列幅比率を確認し、横方向のはみ出しは検出されなかった。
- ブラウザーには生成HTMLとCSSだけを渡した。画像リクエスト216件を遮断し、画像・faviconの取得、スクリーンショット、画像解析は実施していない。
- `scripts/verify-build.py` はPython標準ライブラリのみを使用する。PDFとの照合は `tmp/spec-text` がある場合に実行する。

## 仕様書に従って実装した内容

- 正式サイト名は最新指示の「べちぱーCup Vol.1」。HTMLタイトルの接尾辞は仕様書の「｜べちぱーCup」を維持。
- ページ管理台帳20261030版のURL・階層、画像管理台帳20261031版のID・ファイル名を使用。
- 共通ヘッダー、4項目メニュー、3要素フッターをAstro部品で一元化。ヘッダーはスクロール追従なし。パンくずなし。
- 文字リンクの通常色・hover色・背景色、画像リンクのhoverなし・アニメーションなしを実装。
- 画像は通常のimg要素で `images-stg` のURLを参照。画像最適化・画像importなし。
- PG-002：画像左／本文右のPC構成、SP縦配置、お知らせ1件・最大5件の選別、画像リンク5件、文字リンク4件、大会結果の非表示。
- PG-004：情報枠4件、PCの大会形式／日時2列、SP縦配置、画像リンク3件と指定の余白・最小高さ。
- PG-005：表頭なし2列7行、指定の背景交互色、PC22:78／SP35:65、SPだけの画像リンク共通外枠、暫定採用寸法。
- PG-006：12＋11の23カード、PC2列／SP1列、＋は装飾のみ、マップ①～⑤、問合せフォームの文字列だけのリンク、画像リンク2件、親ページ戻り。
- PG-007：指定8件、禁止17行、PC44:56／SP縦、2列6データ行、PC27:73／SP37:63、親ページ戻り。
- PG-008：Tier画像参照、2列7データ行、PC31:69／SP36:64、担当者4文・禁止アドオン9行、親ページ戻り。「神代リゼ」などの承認表記を保持。
- PG-009：日程画像1枚を参照しHTML表へ変換しない。IMG-016案内はPC25:75／SP縦、リンク用a要素・カーソル・hoverなし。
- 960px以下／961px以上の切替を全ページに適用。ページ別の枠線・画像枠比率・ラベル高さを保持。

## 未実装・未確認・資料上の留意点

1. **画像の内容・配信状態・実表示は未確認。** 画像を取得せずURL・alt・指定寸法だけを実装した。画像が必要なTier分類・日程本文の代替作成は行っていない。画像を含む最終外観確認はユーザー側で必要。
2. **favicon／OGP本体は制作未完了。** faviconはNo.16どおり3参照だけを出力。完成して表示されることは保証していない。台帳のIMG-020_favicon.pngと実使用3ファイルの管理上の対応は、資料で保留とされている。StagingにOGPを出力していない。
3. **文字情報だけでは確定できない外観がある。** 共通部品の余白・メニュー間隔、ページタイトルや一部見出し・本文の文字サイズ、未数値化の枠角丸・装飾・セクション間隔、PG-002の文字リンク4件の厳密なPC上下左右配置などは、資料が案図参照のみの箇所を含む。画像を解析せず、見出し階層のブラウザー標準表示と本文記載順を使っている。案図との完全一致として承認済みとは扱えない。追加の文字・数値指定が必要。
4. **PG-005は暫定値。** 仕様書にある数値を実装したが、ユーザーによるStaging照合・承認前に最終確定値として扱わない。
5. **対象外ページへのリンク。** 次の既決の有効リンクを保持したが、この制作ではリンク先HTMLを作っていないため遷移後の表示は確認できない。ローカルの今回成果物だけではリンク先は存在しない。

| 参照元 | 対象外の遷移先 |
| --- | --- |
| 通常7ページの共通メニュー | PG-010 参加者、PG-014 大会当日 |
| PG-002の画像リンク | PG-010 参加者、PG-014 大会当日 |
| PG-002の文字リンク | PG-021 お問い合わせ・よくある質問、PG-020 運営者紹介、PG-019 注意事項・免責事項、PG-022 プライバシー・権利情報 |
| PG-004の画像リンク | PG-011 募集要項 |
| PG-006の「問合せフォーム」 | PG-021 お問い合わせ・よくある質問 |

6. **一般規則と今回範囲の差。** 全体仕様の「未公開ページへのリンクを有効化しない」と、個別ページの「初版リンクは有効」という記載があり、今回の制作範囲は初版全14ページより狭い。最新指示に従い既決リンク先・条件を変更せず、上表で未確認を明示した。PG-015案内は指定どおり無効。
7. **ローカル画像配信の設定は未実装。** 今回はStaging専用としてimages-stg参照を生成した。資料のローカル画像サーバーの具体的URL・ポート・パスは未指定であり、推測設定していない。本番向け設定・OGP生成への拡張は今回行っていない。
8. **リモートStagingの表示・公開設定は未確認。** Push・公開をしていない。開発サーバーは起動していない。

## 画像を触らないためのビルド方法

既存の `public/favicon.ico`・`public/favicon.svg` と `docs/favicon.ico`・`docs/favicon.svg` は作業開始時から存在した。画像の削除・移動・コピーも行わず、そのまま残した。生成HTMLはこれらを参照しない。

標準の `astro build` はpublicのコピーとdocsの消去を伴うため、`scripts/build.mjs` からAstroのbuild APIを呼び出す。public/.nojekyllだけを作業用publicディレクトリへコピーし、これをビルド時publicDirに指定する。`vite.build.emptyOutDir: false` で既存docs画像の消去を防ぐ。`astro.config.mjs` および既存のsite・base・outDirは変更していない。

この保護のため出力先全体は自動消去しない。将来のページ削除・URL変更時には、古い生成物を別途精査する必要がある。今回はHTMLが対象8件だけであることを検証し、この作業中に発生した未参照の旧CSSだけを除去した。

## Git差分・Commit候補

作業開始時点で `git ls-files` は0件で、初期プロジェクトも全て未追跡だった。そのため、通常の `git diff`・`git diff --stat` は空であり、今回変更がないことを意味しない。履歴との差分は算出できない。作業開始時の一覧と本報告の新規／変更一覧で区別している。`git diff --cached` も空で、ステージ済み変更なし。

今回のCommit候補は上記の新規ソース・変更3ファイル（.gitignore、package.json、src/pages/index.astro）、本報告、public/.nojekyll、生成HTML8件・CSS・docs/.nojekyll。初回Commitに必要となる既存のastro.config.mjs、package-lock.json、tsconfig.json等は、今回の変更とは別にユーザーが確認する対象。

Commit候補から除外：すべての画像ファイル、codex-input内9資料、tmp、node_modules、.astro。既存の画像4ファイルが `git status` に出るが、今回の新規制作物・Commit候補には含めない。

対象外ページ・資料・画像・既存設定ファイル・依存ロック・README・エディター設定は変更していない。git add、git commit、git push、本番反映、画像専用リポジトリ操作、GitHub Pages設定変更は未実施。ユーザーの確認・承認待ちで停止する。
