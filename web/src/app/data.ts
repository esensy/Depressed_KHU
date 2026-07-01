export const STATS = {
  totalPosts: 6568,
  yearRange: "2019 – 2023",
  avgDailyPosts2023: 4.4,
  avgLikes: 0.84,
  avgComments: 1.9,
  avgScraps: 0.14,
};

export const YEARLY_POSTS = [
  { year: "2019", count: 751 },
  { year: "2020", count: 1089 },
  { year: "2021", count: 1372 },
  { year: "2022", count: 1614 },
  { year: "2023", count: 1742 },
];

export const MONTHLY_AVG = [
  { month: "1월",  count: 98 },
  { month: "2월",  count: 89 },
  { month: "3월",  count: 145 },
  { month: "4월",  count: 138 },
  { month: "5월",  count: 122 },
  { month: "6월",  count: 101 },
  { month: "7월",  count: 88 },
  { month: "8월",  count: 84 },
  { month: "9월",  count: 97 },
  { month: "10월", count: 103 },
  { month: "11월", count: 108 },
  { month: "12월", count: 95 },
];

export const HOURLY_AVG = [
  { hour: "0시",  count: 52 },
  { hour: "1시",  count: 68 },
  { hour: "2시",  count: 71 },
  { hour: "3시",  count: 58 },
  { hour: "4시",  count: 33 },
  { hour: "5시",  count: 18 },
  { hour: "6시",  count: 12 },
  { hour: "7시",  count: 15 },
  { hour: "8시",  count: 22 },
  { hour: "9시",  count: 31 },
  { hour: "10시", count: 38 },
  { hour: "11시", count: 44 },
  { hour: "12시", count: 48 },
  { hour: "13시", count: 45 },
  { hour: "14시", count: 43 },
  { hour: "15시", count: 41 },
  { hour: "16시", count: 42 },
  { hour: "17시", count: 46 },
  { hour: "18시", count: 49 },
  { hour: "19시", count: 53 },
  { hour: "20시", count: 59 },
  { hour: "21시", count: 62 },
  { hour: "22시", count: 64 },
  { hour: "23시", count: 58 },
];

export const CLUSTERS = [
  {
    id: 0,
    label: "가족 갈등",
    keywords: ["엄마", "가족", "부모님", "집"],
    description: "가족과의 관계 문제, 특히 부모와의 갈등이 우울감의 주요 원인으로 나타남",
    color: "#6366f1",
  },
  {
    id: 1,
    label: "학업 스트레스",
    keywords: ["공부", "학점", "시험", "성적"],
    description: "학업 부담과 성취 압박으로 인한 스트레스",
    color: "#8b5cf6",
  },
  {
    id: 2,
    label: "정신건강 도움 요청",
    keywords: ["정신과", "병원", "상담", "약"],
    description: "전문적 도움을 찾는 게시글 — 정신과 방문 경험 공유 및 문의",
    color: "#a78bfa",
  },
  {
    id: 3,
    label: "대인관계",
    keywords: ["친구", "사람", "관계", "외로움"],
    description: "대인관계 어려움, 고립감, 외로움을 호소하는 게시글",
    color: "#c4b5fd",
  },
  {
    id: 4,
    label: "자기 감정 표현",
    keywords: ["죽고", "힘들다", "살기", "싫다"],
    description: "직접적인 감정 표현 — 극단적 생각 포함, 위기 신호와 연관",
    color: "#ddd6fe",
  },
];

export const HYPOTHESES = [
  {
    id: 1,
    title: "봄에 게시판 활발도가 가장 높다",
    result: "검증됨",
    detail:
      "3–5월 게시글 활발도가 다른 계절 대비 통계적으로 유의미하게 높음 (p < 0.05). 개강, 과제, 인간관계 재편이 복합적으로 작용.",
    verdict: true,
  },
  {
    id: 2,
    title: "주요 주제는 취업·학점일 것이다",
    result: "기각됨",
    detail:
      "K-means 클러스터링 결과 실제 주요 주제는 '가족', '정신과', '공부' 순. 취업보다 가족 갈등과 정신건강이 더 핵심적 주제.",
    verdict: false,
  },
  {
    id: 3,
    title: "새벽 시간대에 게시글이 집중된다",
    result: "검증됨",
    detail:
      "오전 1–3시 게시글 비율이 낮 시간대보다 유의미하게 높음. 혼자 있는 밤 시간에 감정을 표현하는 경향.",
    verdict: true,
  },
];
