"use client";

import {
  BarChart, Bar, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell,
} from "recharts";
import { STATS, YEARLY_POSTS, MONTHLY_AVG, HOURLY_AVG, CLUSTERS, HYPOTHESES } from "./data";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-950 text-gray-100 font-sans">
      {/* 헤더 */}
      <header className="border-b border-gray-800 px-8 py-6">
        <p className="text-xs text-indigo-400 tracking-widest uppercase mb-1">경희대학교 에브리타임</p>
        <h1 className="text-2xl font-bold text-white">우울증 게시판 패턴 분석</h1>
        <p className="text-sm text-gray-400 mt-1">{STATS.yearRange} · 총 {STATS.totalPosts.toLocaleString()}개 게시글</p>
      </header>

      <div className="max-w-6xl mx-auto px-8 py-10 space-y-16">

        {/* 요약 지표 */}
        <section>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "총 게시글", value: STATS.totalPosts.toLocaleString(), unit: "개" },
              { label: "2023년 일평균", value: STATS.avgDailyPosts2023, unit: "개/일" },
              { label: "평균 댓글 수", value: STATS.avgComments, unit: "개" },
              { label: "가장 활발한 시간", value: "오전 2시", unit: "" },
            ].map((s) => (
              <div key={s.label} className="bg-gray-900 rounded-xl p-5 border border-gray-800">
                <p className="text-xs text-gray-500 mb-2">{s.label}</p>
                <p className="text-3xl font-bold text-indigo-400">{s.value}<span className="text-sm text-gray-400 ml-1">{s.unit}</span></p>
              </div>
            ))}
          </div>
        </section>

        {/* 연도별 추이 */}
        <section>
          <h2 className="text-lg font-semibold mb-1">연도별 게시글 수</h2>
          <p className="text-sm text-gray-400 mb-6">2019년부터 꾸준히 증가 — 우울증 유병률 상승과 같은 추세</p>
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={YEARLY_POSTS} barSize={40}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                <XAxis dataKey="year" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip contentStyle={{ background: "#111827", border: "1px solid #374151", borderRadius: 8 }} />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {YEARLY_POSTS.map((_, i) => (
                    <Cell key={i} fill={`hsl(${240 + i * 15}, 70%, ${50 + i * 5}%)`} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* 월별 + 시간대 */}
        <section className="grid md:grid-cols-2 gap-6">
          <div>
            <h2 className="text-lg font-semibold mb-1">월별 평균 게시글 수</h2>
            <p className="text-sm text-gray-400 mb-4">3–5월(봄)에 집중적으로 증가</p>
            <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={MONTHLY_AVG} barSize={16}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                  <XAxis dataKey="month" stroke="#6b7280" tick={{ fontSize: 11 }} />
                  <YAxis stroke="#6b7280" />
                  <Tooltip contentStyle={{ background: "#111827", border: "1px solid #374151", borderRadius: 8 }} />
                  <Bar dataKey="count" fill="#6366f1" radius={[3, 3, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div>
            <h2 className="text-lg font-semibold mb-1">시간대별 게시글 수</h2>
            <p className="text-sm text-gray-400 mb-4">새벽 1–3시에 가장 많은 게시글 작성</p>
            <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={HOURLY_AVG}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                  <XAxis dataKey="hour" stroke="#6b7280" tick={{ fontSize: 10 }} interval={3} />
                  <YAxis stroke="#6b7280" />
                  <Tooltip contentStyle={{ background: "#111827", border: "1px solid #374151", borderRadius: 8 }} />
                  <Line type="monotone" dataKey="count" stroke="#a78bfa" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </section>

        {/* 가설 검증 */}
        <section>
          <h2 className="text-lg font-semibold mb-1">가설 검증 결과</h2>
          <p className="text-sm text-gray-400 mb-6">통계 분석으로 검증한 3가지 가설</p>
          <div className="space-y-4">
            {HYPOTHESES.map((h) => (
              <div key={h.id} className="bg-gray-900 rounded-xl p-6 border border-gray-800 flex gap-5">
                <div className={`mt-1 flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold
                  ${h.verdict ? "bg-indigo-500 text-white" : "bg-gray-700 text-gray-400"}`}>
                  {h.verdict ? "✓" : "✗"}
                </div>
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-sm font-medium text-gray-200">가설 {h.id}</span>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium
                      ${h.verdict ? "bg-indigo-900 text-indigo-300" : "bg-gray-800 text-gray-400"}`}>
                      {h.result}
                    </span>
                  </div>
                  <p className="font-semibold text-white mb-1">"{h.title}"</p>
                  <p className="text-sm text-gray-400">{h.detail}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* 토픽 클러스터 */}
        <section>
          <h2 className="text-lg font-semibold mb-1">주제 군집 분석 (K-means, k=5)</h2>
          <p className="text-sm text-gray-400 mb-6">TF-IDF + K-means 클러스터링으로 도출한 5개 주제</p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {CLUSTERS.map((c) => (
              <div key={c.id} className="bg-gray-900 rounded-xl p-5 border border-gray-800">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-3 h-3 rounded-full" style={{ background: c.color }} />
                  <span className="font-semibold text-sm">{c.label}</span>
                </div>
                <div className="flex flex-wrap gap-2 mb-3">
                  {c.keywords.map((kw) => (
                    <span key={kw} className="text-xs bg-gray-800 text-gray-300 px-2 py-1 rounded-md">{kw}</span>
                  ))}
                </div>
                <p className="text-xs text-gray-500">{c.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* 인사이트 */}
        <section className="bg-gray-900 rounded-xl p-8 border border-gray-800">
          <h2 className="text-lg font-semibold mb-6">핵심 인사이트</h2>
          <ul className="space-y-4 text-sm text-gray-300">
            {[
              "우울증 게시글 수는 2019년 이후 매년 증가세 — 대학생 정신건강 문제가 심화되는 추세",
              "봄 학기 초(3–4월)에 게시글이 급증 — 새 학기 적응, 관계 재편, 과제 압박이 복합 작용",
              "새벽 1–3시에 게시글 집중 — 혼자 있는 시간에 감정이 표출되는 패턴",
              "주요 주제는 취업·학점이 아닌 가족 갈등, 정신과 상담, 대인관계 — 예상을 뒤집는 결과",
              "많은 학생이 정신과 방문을 고민하지만 진료기록 우려로 망설이는 현실이 게시글에 드러남",
            ].map((insight, i) => (
              <li key={i} className="flex gap-3">
                <span className="text-indigo-400 flex-shrink-0">→</span>
                <span>{insight}</span>
              </li>
            ))}
          </ul>
        </section>

      </div>

      <footer className="border-t border-gray-800 px-8 py-6 text-center text-xs text-gray-600">
        경희대학교 에브리타임 우울증 게시판 데이터 분석 · 2020105729 임성은
      </footer>
    </main>
  );
}
