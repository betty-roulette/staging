import path from 'node:path';

export const siteName = 'べちぱーCup Vol.1';
export const description = 'Dead by Daylight で開催する「べちぱーCup」の大会情報を掲載する Web サイトです。大会概要、ルール、スケジュール、参加者情報、大会当日の案内、大会結果などをご案内します。';

// Page ledger 20261030: routes for out-of-scope destinations are references only.
export const pages = {
  'PG-001': ['トップページ', '/'],
  'PG-002': [siteName, '/betipercup/'],
  'PG-004': ['大会概要', '/betipercup/overview/'],
  'PG-005': ['大会ルール概要・詳細', '/betipercup/rules/'],
  'PG-006': ['大会ルール詳細', '/betipercup/rules/detail/'],
  'PG-007': ['サバイバー：ルール', '/betipercup/rules/survivor/'],
  'PG-008': ['キラー：ルール', '/betipercup/rules/killer/'],
  'PG-009': ['スケジュール：全体', '/betipercup/schedule/'],
  'PG-010': ['参加者', '/betipercup/participants/'],
  'PG-011': ['募集要項', '/betipercup/participants/recruitment/'],
  'PG-014': ['大会当日', '/betipercup/event/'],
  'PG-015': ['大会当日スケジュール', '/betipercup/event/schedule/'],
  'PG-019': ['注意事項・免責事項', '/betipercup/notice/'],
  'PG-020': ['運営者紹介', '/betipercup/organizer/'],
  'PG-021': ['お問い合わせ・よくある質問', '/betipercup/faq/'],
  'PG-022': ['プライバシー・権利情報', '/betipercup/privacy/'],
  'PG-024': ['協賛・賞金', '/betipercup/sponsors-prizes/'],
} as const;
export type PageId = keyof typeof pages;

export function href(from: PageId, to: PageId) {
  const relative = path.posix.relative(pages[from][1], pages[to][1]);
  return relative ? `${relative}/` : './';
}

// String references only. No imports, requests, transforms, or image metadata reads.
export const imageBase = 'https://betty-roulette.github.io/images-stg/';
export const images = {
  'IMG-001': ['IMG-001_header.png', '大会サイトのヘッダー画像'],
  'IMG-002': ['IMG-002_main.png', 'べちぱーCup Vol.1の大会メイン画像'],
  'IMG-003': ['IMG-003_overview.png', '大会概要へのリンク'],
  'IMG-004': ['IMG-004_rules.png', '大会ルール概要・詳細へのリンク'],
  'IMG-005': ['IMG-005_details.png', '大会ルール詳細へのリンク'],
  'IMG-006': ['IMG-006_survivor.png', 'サバイバー：ルールへのリンク'],
  'IMG-007': ['IMG-007_killer.png', 'キラー：ルールへのリンク'],
  'IMG-008': ['IMG-008_schedule.png', 'スケジュールへのリンク'],
  'IMG-009': ['IMG-009_players.png', '参加者ページへのリンク'],
  'IMG-010': ['IMG-010_entry.png', '募集要項へのリンク'],
  'IMG-011': ['IMG-011_event.png', '大会当日ページへのリンク'],
  'IMG-012': ['IMG-012_tier.png', 'キラーTier表'],
  'IMG-013': ['IMG-013_timeline.png', '大会全体の日程・主要予定'],
  'IMG-014': ['IMG-014_intro.png', '参加者紹介'],
  'IMG-015': ['IMG-015_bracket.png', '対戦表'],
  'IMG-016': ['IMG-016_agenda.png', '大会当日スケジュール'],
  'IMG-017': ['IMG-017_stream.png', '配信情報'],
  'IMG-022': ['IMG-022_sponsor.png', '協賛・賞金'],
  'IMG-801': ['IMG-801_sponsor-01.png', '協賛：ROH'],
  'IMG-802': ['IMG-802_sponsor-02.png', '協賛：匿名'],
  'IMG-803': ['IMG-803_sponsor-03.png', '協賛：KARINGA'],
} as const;
export type ImageId = keyof typeof images;
