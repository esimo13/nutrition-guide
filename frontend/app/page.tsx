"use client";

import { useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";

type FormState = {
  age: string;
  district: string;
  trimester: "1" | "2" | "3";
  bmi: string;
  blood_pressure: "Normal" | "High";
  history_diabetes: boolean;
  history_anemia: boolean;
  current_season: "Monsoon" | "Winter" | "Summer";
};

type ApiResponse = {
  response: string;
  predicted_calories?: number;
  predicted_iron_tier?: string;
  recommended_foods?: string[];
};

const DISTRICTS = [
  "Dhaka",
  "Khulna",
  "Sylhet",
  "Rajshahi",
  "Barisal",
  "Chittagong",
  "Rangpur",
  "Mymensingh",
];

export default function HomePage() {
  const [form, setForm] = useState<FormState>({
    age: "24",
    district: "Dhaka",
    trimester: "2",
    bmi: "21.5",
    blood_pressure: "Normal",
    history_diabetes: false,
    history_anemia: true,
    current_season: "Monsoon",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ApiResponse | null>(null);

  const payload = useMemo(
    () => ({
      age: Number(form.age),
      district: form.district,
      trimester: Number(form.trimester),
      bmi: Number(form.bmi),
      blood_pressure: form.blood_pressure,
      history_diabetes: form.history_diabetes ? 1 : 0,
      history_anemia: form.history_anemia ? 1 : 0,
      current_season: form.current_season,
    }),
    [form]
  );

  const handleChange = (
    key: keyof FormState,
    value: string | boolean
  ) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || "Request failed");
      }

      const data = (await response.json()) as ApiResponse;
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_#fef3c7,_#fdf2f8_45%,_#e0f2fe)] text-slate-900">
      <div className="mx-auto flex min-h-screen w-full max-w-6xl flex-col gap-10 px-6 py-12 lg:flex-row">
        <section className="flex-1">
          <div className="rounded-3xl border border-white/60 bg-white/80 p-8 shadow-[0_24px_80px_-40px_rgba(15,23,42,0.45)] backdrop-blur">
            <p className="text-xs uppercase tracking-[0.35em] text-amber-700">
              Maternal Nutrition Assistant
            </p>
            <h1 className="mt-4 text-3xl font-semibold tracking-tight text-slate-900">
              Personalized Pregnancy Nutrition Guidance
            </h1>
            <p className="mt-3 text-sm text-slate-600">
              Provide the mother profile details and receive a Bangla summary
              crafted by the clinical nutrition assistant.
            </p>

            <div className="mt-8 grid gap-5 md:grid-cols-2">
              <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                Age
                <input
                  type="number"
                  value={form.age}
                  onChange={(event) => handleChange("age", event.target.value)}
                  className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm shadow-sm focus:border-amber-400 focus:outline-none"
                />
              </label>

              <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                District
                <select
                  value={form.district}
                  onChange={(event) => handleChange("district", event.target.value)}
                  className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm shadow-sm focus:border-amber-400 focus:outline-none"
                >
                  {DISTRICTS.map((district) => (
                    <option key={district} value={district}>
                      {district}
                    </option>
                  ))}
                </select>
              </label>

              <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                Trimester
                <select
                  value={form.trimester}
                  onChange={(event) =>
                    handleChange("trimester", event.target.value)
                  }
                  className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm shadow-sm focus:border-amber-400 focus:outline-none"
                >
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                </select>
              </label>

              <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                BMI
                <input
                  type="number"
                  step="0.1"
                  value={form.bmi}
                  onChange={(event) => handleChange("bmi", event.target.value)}
                  className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm shadow-sm focus:border-amber-400 focus:outline-none"
                />
              </label>

              <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                Blood Pressure
                <select
                  value={form.blood_pressure}
                  onChange={(event) =>
                    handleChange("blood_pressure", event.target.value)
                  }
                  className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm shadow-sm focus:border-amber-400 focus:outline-none"
                >
                  <option value="Normal">Normal</option>
                  <option value="High">High</option>
                </select>
              </label>

              <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                Current Season
                <select
                  value={form.current_season}
                  onChange={(event) =>
                    handleChange("current_season", event.target.value)
                  }
                  className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm shadow-sm focus:border-amber-400 focus:outline-none"
                >
                  <option value="Monsoon">Monsoon</option>
                  <option value="Winter">Winter</option>
                  <option value="Summer">Summer</option>
                </select>
              </label>
            </div>

            <div className="mt-6 grid gap-4 rounded-2xl border border-dashed border-amber-200 bg-amber-50/60 p-4 text-sm text-slate-700 md:grid-cols-2">
              <label className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={form.history_diabetes}
                  onChange={(event) =>
                    handleChange("history_diabetes", event.target.checked)
                  }
                  className="h-4 w-4 accent-amber-600"
                />
                History of Diabetes
              </label>
              <label className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={form.history_anemia}
                  onChange={(event) =>
                    handleChange("history_anemia", event.target.checked)
                  }
                  className="h-4 w-4 accent-amber-600"
                />
                History of Anemia
              </label>
            </div>

            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
              className="mt-8 w-full rounded-2xl bg-slate-900 px-6 py-3 text-sm font-semibold uppercase tracking-[0.3em] text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {loading ? "Generating..." : "Submit"}
            </button>

            {error && (
              <p className="mt-4 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-600">
                {error}
              </p>
            )}
          </div>
        </section>

        <section className="flex-1">
          <div className="flex h-full flex-col gap-6 rounded-3xl border border-slate-200 bg-white/70 p-8 shadow-[0_28px_70px_-50px_rgba(15,23,42,0.4)] backdrop-blur">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-slate-500">
                AI Recommendation
              </p>
              <h2 className="mt-3 text-2xl font-semibold text-slate-900">
                Bangla Nutrition Summary
              </h2>
              <p className="mt-2 text-sm text-slate-600">
                The response below mirrors the explanation delivered by the
                clinical dietitian assistant.
              </p>
            </div>

            <div className="flex-1 rounded-2xl border border-slate-200 bg-white p-6">
              {loading && (
                <div className="flex h-full flex-col items-center justify-center gap-4 text-slate-600">
                  <div className="relative h-14 w-14">
                    <div className="absolute inset-0 rounded-full border-4 border-amber-200" />
                    <div className="absolute inset-0 rounded-full border-4 border-amber-600 border-t-transparent animate-spin" />
                  </div>
                  <p className="text-sm">Preparing your personalized guidance...</p>
                </div>
              )}

              {!loading && !result && (
                <div className="flex h-full flex-col items-center justify-center gap-3 text-center text-sm text-slate-500">
                  <span className="inline-flex rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs uppercase tracking-[0.3em] text-amber-700">
                    Awaiting Submission
                  </span>
                  <p>
                    Submit the profile form to see the Bangla recommendation
                    and food guidance here.
                  </p>
                </div>
              )}

              {!loading && result && (
                <div className="space-y-4">
                  <div className="flex flex-wrap gap-3 text-xs text-slate-600">
                    {result.predicted_calories !== undefined && (
                      <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1">
                        Calories: {result.predicted_calories}
                      </span>
                    )}
                    {result.predicted_iron_tier && (
                      <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1">
                        Iron tier: {result.predicted_iron_tier}
                      </span>
                    )}
                    {result.recommended_foods && result.recommended_foods.length > 0 && (
                      <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1">
                        Foods: {result.recommended_foods.join(", ")}
                      </span>
                    )}
                  </div>

                  <div className="prose prose-sm max-w-none text-slate-700">
                    <ReactMarkdown>{result.response}</ReactMarkdown>
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
