import json

with open("model_data.json", "r", encoding="utf-8") as f:
    model_data_raw = f.read()

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>50 Startups Multiple Linear Regression Explorer — CRISP-DM Feature Selection</title>
  <meta name="description" content="50 Startups Multiple Linear Regression Explorer: Feature Selection & Parsimony Analysis across 5 ML algorithms (Lasso, Forward SFS, RFE, ElasticNet, Exhaustive Search)." />
  
  <!-- Google Fonts: Outfit (Headings), Inter (Body), JetBrains Mono (Numbers/Code) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet" />
  
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.2/dist/chart.umd.min.js"></script>

  <style>
    /* ─── Global Design Tokens: Midnight Deep Blue Theme ─── */
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    :root {
      --bg-dark: #070b14;
      --bg-space: #0b1224;
      --bg-space-card: rgba(13, 22, 42, 0.76);
      --bg-space-card-hover: rgba(20, 33, 62, 0.85);
      --bg-elevated: #111c38;
      
      --border: rgba(99, 102, 241, 0.2);
      --border-subtle: rgba(148, 163, 184, 0.12);
      --border-hover: rgba(99, 102, 241, 0.5);
      --border-glow: rgba(99, 102, 241, 0.35);

      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --text-light: #cbd5e1;

      /* Cosmic Accent Colors */
      --indigo-500: #6366f1;
      --indigo-400: #818cf8;
      --indigo-glow: rgba(99, 102, 241, 0.35);
      
      --cyan-500: #06b6d4;
      --cyan-400: #22d3ee;
      --cyan-glow: rgba(6, 182, 212, 0.35);

      --emerald-500: #10b981;
      --emerald-400: #34d399;
      --emerald-glow: rgba(16, 185, 129, 0.35);

      --amber-500: #f59e0b;
      --amber-400: #fbbf24;
      --amber-glow: rgba(245, 158, 11, 0.35);

      --rose-500: #f43f5e;
      --rose-400: #fb7185;
      --rose-glow: rgba(244, 63, 94, 0.35);

      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-heading: 'Outfit', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;

      --radius-sm: 8px;
      --radius-md: 12px;
      --radius: 16px;
      --radius-lg: 20px;

      --shadow-glass: 0 8px 32px 0 rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.08);
      --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.35);
      --shadow-glow: 0 0 25px rgba(99, 102, 241, 0.25);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #080d1a;
    }
    ::-webkit-scrollbar-thumb {
      background: #1e293b;
      border-radius: 4px;
      border: 1px solid rgba(99, 102, 241, 0.2);
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #334155;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 12% 15%, rgba(49, 46, 129, 0.35) 0%, transparent 45%),
        radial-gradient(circle at 85% 20%, rgba(6, 182, 212, 0.14) 0%, transparent 40%),
        radial-gradient(circle at 50% 85%, rgba(16, 185, 129, 0.1) 0%, transparent 50%),
        linear-gradient(180deg, #070b14 0%, #0a1020 40%, #060913 100%);
      background-attachment: fixed;
      color: var(--text-main);
      line-height: 1.6;
      min-height: 100vh;
      padding-bottom: 70px;
      -webkit-font-smoothing: antialiased;
    }

    .container {
      max-width: 1320px;
      margin: 0 auto;
      padding: 24px 24px 0;
    }

    /* ─── Breadcrumb ─── */
    .breadcrumb {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-bottom: 14px;
    }

    .breadcrumb a {
      color: var(--text-muted);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s;
    }

    .breadcrumb a:hover {
      color: var(--cyan-400);
      text-shadow: 0 0 10px var(--cyan-glow);
    }

    .breadcrumb .sep {
      color: var(--text-dim);
      font-size: 0.75rem;
    }

    .breadcrumb .current {
      color: var(--text-main);
      font-weight: 600;
    }

    /* ─── Top Header ─── */
    .top-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .title-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .title-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(6, 182, 212, 0.25));
      border: 1px solid rgba(99, 102, 241, 0.4);
      color: var(--cyan-400);
      font-size: 1.25rem;
      box-shadow: 0 0 18px var(--indigo-glow);
    }

    .main-title {
      font-family: var(--font-heading);
      font-size: 1.55rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #ffffff 30%, #93c5fd 75%, #a5b4fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .badge-crisp {
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(16, 185, 129, 0.2));
      border: 1px solid rgba(99, 102, 241, 0.5);
      color: #e0e7ff;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 4px 11px;
      border-radius: 999px;
      letter-spacing: 0.05em;
      cursor: pointer;
      transition: all 0.25s;
      box-shadow: 0 0 14px rgba(99, 102, 241, 0.2);
    }

    .badge-crisp:hover {
      background: var(--indigo-500);
      color: #ffffff;
      border-color: var(--indigo-400);
      box-shadow: 0 0 20px var(--indigo-glow);
      transform: translateY(-1px);
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .btn-outline {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border);
      color: var(--text-light);
      font-size: 0.82rem;
      font-weight: 600;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      backdrop-filter: blur(8px);
      box-shadow: var(--shadow-card);
      transition: all 0.2s ease;
      text-decoration: none;
    }

    .btn-outline:hover {
      background: rgba(30, 41, 59, 0.8);
      border-color: var(--border-hover);
      color: #ffffff;
      box-shadow: 0 0 16px rgba(99, 102, 241, 0.3);
      transform: translateY(-1px);
    }

    /* ─── Hero Banner: Deep Blue Celestial Glass ─── */
    .hero-card {
      background: linear-gradient(135deg, rgba(20, 24, 52, 0.85) 0%, rgba(13, 21, 40, 0.92) 50%, rgba(7, 26, 44, 0.85) 100%);
      border: 1px solid rgba(99, 102, 241, 0.28);
      border-radius: var(--radius-lg);
      padding: 36px 42px;
      color: #ffffff;
      box-shadow: var(--shadow-glass), 0 0 35px rgba(99, 102, 241, 0.18);
      margin-bottom: 24px;
      position: relative;
      overflow: hidden;
      backdrop-filter: blur(16px);
    }

    .hero-card::before {
      content: '';
      position: absolute;
      top: -60%;
      right: -20%;
      width: 400px;
      height: 400px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.18) 0%, transparent 70%);
      border-radius: 50%;
      pointer-events: none;
    }

    .hero-title {
      font-family: var(--font-heading);
      font-size: 2.15rem;
      font-weight: 800;
      letter-spacing: -0.025em;
      margin-bottom: 12px;
      line-height: 1.2;
      background: linear-gradient(135deg, #ffffff 40%, #bae6fd 80%, #a7f3d0 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-desc {
      font-size: 0.98rem;
      color: #cbd5e1;
      max-width: 980px;
      line-height: 1.65;
      margin-bottom: 24px;
    }

    .hero-desc code {
      font-family: var(--font-mono);
      background: rgba(99, 102, 241, 0.22);
      border: 1px solid rgba(129, 140, 248, 0.3);
      color: #e0e7ff;
      padding: 2px 7px;
      border-radius: 5px;
      font-size: 0.9em;
    }

    .hero-badges {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
    }

    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      background: rgba(255, 255, 255, 0.06);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 999px;
      padding: 6px 16px;
      font-size: 0.82rem;
      font-weight: 600;
      color: #e2e8f0;
      transition: all 0.2s;
    }

    .hero-badge:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.25);
    }

    .hero-badge.highlight-sweet {
      background: rgba(16, 185, 129, 0.16);
      border-color: rgba(52, 211, 153, 0.45);
      color: #6ee7b7;
      box-shadow: 0 0 16px rgba(16, 185, 129, 0.25);
    }

    .hero-badge.highlight-cliff {
      background: rgba(245, 158, 11, 0.16);
      border-color: rgba(251, 191, 36, 0.45);
      color: #fde68a;
      box-shadow: 0 0 16px rgba(245, 158, 11, 0.2);
    }

    /* ─── Control Cards ─── */
    .control-card {
      background: var(--bg-space-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px 26px;
      margin-bottom: 16px;
      box-shadow: var(--shadow-glass);
      backdrop-filter: blur(16px);
      transition: border-color 0.25s, box-shadow 0.25s;
    }

    .control-card:hover {
      border-color: var(--border-hover);
      box-shadow: var(--shadow-glass), var(--shadow-glow);
    }

    .section-label {
      font-size: 0.74rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: var(--cyan-400);
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 14px;
    }

    .pill-group {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .btn-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(20, 31, 58, 0.65);
      border: 1.5px solid var(--border);
      color: var(--text-light);
      padding: 9px 20px;
      border-radius: 999px;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      user-select: none;
      backdrop-filter: blur(8px);
    }

    .btn-pill:hover {
      border-color: var(--border-hover);
      background: rgba(30, 45, 82, 0.8);
      color: #ffffff;
      transform: translateY(-1px);
    }

    .btn-pill .sub-tag {
      font-size: 0.72rem;
      padding: 2px 8px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-muted);
      font-weight: 500;
      transition: all 0.2s;
    }

    /* Selected Algorithm Pill */
    .btn-pill.selected-algo {
      background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
      border-color: #818cf8;
      color: #ffffff;
      box-shadow: 0 0 20px rgba(99, 102, 241, 0.45);
    }

    .btn-pill.selected-algo .sub-tag {
      background: rgba(255, 255, 255, 0.22);
      color: #ffffff;
    }

    /* Selected K Pill: k=2 (Optimal Sweet Spot - Emerald Neon) */
    .btn-pill.selected-k-sweet {
      background: linear-gradient(135deg, #059669 0%, #065f46 100%);
      border-color: #34d399;
      color: #ffffff;
      box-shadow: 0 0 24px rgba(16, 185, 129, 0.55);
    }

    .btn-pill.selected-k-sweet .sub-tag {
      background: rgba(255, 255, 255, 0.25);
      color: #ffffff;
    }

    /* Selected K Pill: Normal k */
    .btn-pill.selected-k-normal {
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      border-color: var(--indigo-400);
      color: #ffffff;
      box-shadow: 0 0 18px rgba(99, 102, 241, 0.35);
    }

    .btn-pill.selected-k-normal .sub-tag {
      background: var(--indigo-500);
      color: #ffffff;
    }

    /* Compare All 5 Methods Button */
    .btn-pill.compare-btn {
      border-style: dashed;
      color: var(--cyan-400);
      border-color: rgba(6, 182, 212, 0.4);
      background: rgba(6, 182, 212, 0.07);
    }

    .btn-pill.compare-btn:hover {
      background: rgba(6, 182, 212, 0.16);
      border-color: var(--cyan-400);
      box-shadow: 0 0 16px var(--cyan-glow);
    }

    .btn-pill.compare-btn.active {
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      border-color: #38bdf8;
      border-style: solid;
      color: #ffffff;
      box-shadow: 0 0 22px rgba(6, 182, 212, 0.5);
    }

    /* ─── Metric Cards Grid ─── */
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
      margin-bottom: 16px;
    }

    @media (max-width: 1120px) {
      .metrics-grid { grid-template-columns: repeat(3, 1fr); }
    }
    @media (max-width: 768px) {
      .metrics-grid { grid-template-columns: 1fr; }
    }

    .metric-card {
      background: var(--bg-space-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px 22px;
      box-shadow: var(--shadow-glass);
      backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 146px;
      position: relative;
      overflow: hidden;
      transition: all 0.25s ease;
    }

    .metric-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent, var(--indigo-400), transparent);
      opacity: 0.6;
    }

    .metric-card:hover {
      transform: translateY(-3px);
      border-color: var(--border-hover);
      box-shadow: var(--shadow-glass), var(--shadow-glow);
    }

    .metric-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 8px;
    }

    .metric-label {
      font-size: 0.74rem;
      font-weight: 700;
      color: var(--text-muted);
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }

    .metric-pill {
      font-size: 0.68rem;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 999px;
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .pill-green {
      background: rgba(16, 185, 129, 0.16);
      color: #34d399;
      border: 1px solid rgba(52, 211, 153, 0.4);
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
    }

    .pill-blue {
      background: rgba(6, 182, 212, 0.16);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.4);
      box-shadow: 0 0 10px rgba(6, 182, 212, 0.2);
    }

    .pill-amber {
      background: rgba(245, 158, 11, 0.16);
      color: #fbbf24;
      border: 1px solid rgba(251, 191, 36, 0.4);
      box-shadow: 0 0 10px rgba(245, 158, 11, 0.2);
    }

    .metric-icon-small {
      color: var(--text-muted);
      font-size: 0.95rem;
    }

    .metric-value {
      font-size: 1.82rem;
      font-weight: 800;
      font-family: var(--font-mono);
      letter-spacing: -0.03em;
      line-height: 1.15;
      margin-bottom: 5px;
      color: #ffffff;
      text-shadow: 0 0 16px rgba(255, 255, 255, 0.15);
    }

    /* Distinct Glows for specific cards */
    #val-rmse { color: #38bdf8; text-shadow: 0 0 15px rgba(56, 189, 248, 0.4); }
    #val-r2 { color: #34d399; text-shadow: 0 0 15px rgba(52, 211, 153, 0.4); }
    #val-adj-r2 { color: #fbbf24; text-shadow: 0 0 15px rgba(251, 191, 36, 0.35); }
    #val-mae { color: #f472b6; text-shadow: 0 0 15px rgba(244, 114, 182, 0.35); }
    #val-f { color: #a78bfa; text-shadow: 0 0 15px rgba(167, 139, 250, 0.35); }

    .metric-desc {
      font-size: 0.77rem;
      color: var(--text-muted);
      line-height: 1.4;
    }

    /* ─── Summary Status Bar ─── */
    .summary-bar {
      background: var(--bg-space-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 14px;
      box-shadow: var(--shadow-glass);
      backdrop-filter: blur(16px);
      margin-bottom: 30px;
    }

    .active-predictors {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .active-predictors-title {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-light);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .feature-tag {
      background: rgba(99, 102, 241, 0.18);
      color: #c7d2fe;
      font-size: 0.8rem;
      font-weight: 600;
      padding: 5px 13px;
      border-radius: 8px;
      border: 1px solid rgba(129, 140, 248, 0.35);
      box-shadow: 0 0 10px rgba(99, 102, 241, 0.15);
    }

    .occam-badge {
      background: rgba(16, 185, 129, 0.14);
      border: 1px solid rgba(52, 211, 153, 0.4);
      color: #6ee7b7;
      padding: 7px 18px;
      border-radius: 999px;
      font-size: 0.84rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      box-shadow: 0 0 16px rgba(16, 185, 129, 0.2);
    }

    /* ─── Tabbed Dashboard Explorer ─── */
    .section-tabs-nav {
      display: flex;
      align-items: center;
      gap: 8px;
      border-bottom: 1px solid var(--border-subtle);
      margin-bottom: 24px;
      overflow-x: auto;
      padding-bottom: 4px;
    }

    .tab-btn {
      background: none;
      border: none;
      font-family: inherit;
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--text-muted);
      padding: 12px 20px;
      border-radius: var(--radius-sm) var(--radius-sm) 0 0;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
      white-space: nowrap;
    }

    .tab-btn:hover {
      color: #ffffff;
      background: rgba(255, 255, 255, 0.03);
    }

    .tab-btn.active {
      color: var(--cyan-400);
      border-bottom-color: var(--cyan-400);
      text-shadow: 0 0 14px var(--cyan-glow);
    }

    .tab-pane {
      display: none;
      animation: fadeIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .tab-pane.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* ─── Chart Containers ─── */
    .chart-grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }

    @media (max-width: 900px) {
      .chart-grid-2 { grid-template-columns: 1fr; }
    }

    .chart-card {
      background: var(--bg-space-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      box-shadow: var(--shadow-glass);
      backdrop-filter: blur(16px);
      transition: all 0.25s;
    }

    .chart-card:hover {
      border-color: var(--border-hover);
      box-shadow: var(--shadow-glass), var(--shadow-glow);
    }

    .chart-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 18px;
    }

    .chart-title {
      font-family: var(--font-heading);
      font-size: 1.05rem;
      font-weight: 700;
      color: #ffffff;
    }

    .chart-subtitle {
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-top: 3px;
    }

    .canvas-wrapper {
      position: relative;
      height: 310px;
      width: 100%;
    }

    /* ─── Equation Callout ─── */
    .equation-box {
      background: rgba(9, 14, 28, 0.9);
      border: 1px solid rgba(6, 182, 212, 0.3);
      border-radius: 12px;
      padding: 20px 26px;
      color: var(--cyan-400);
      font-family: var(--font-mono);
      font-size: 0.98rem;
      overflow-x: auto;
      margin-top: 14px;
      box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.7), 0 0 20px rgba(6, 182, 212, 0.15);
      line-height: 1.6;
    }

    /* ─── What-If Simulator Card ─── */
    .sim-card {
      background: var(--bg-space-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 32px;
      box-shadow: var(--shadow-glass);
      backdrop-filter: blur(16px);
      margin-bottom: 24px;
    }

    .sim-grid {
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      gap: 36px;
      align-items: center;
    }

    @media (max-width: 860px) {
      .sim-grid { grid-template-columns: 1fr; }
    }

    .sim-slider-row {
      margin-bottom: 22px;
    }

    .sim-slider-label-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-light);
    }

    .sim-slider-val {
      font-family: var(--font-mono);
      color: var(--cyan-400);
      font-weight: 700;
      text-shadow: 0 0 10px var(--cyan-glow);
    }

    /* Custom Range Sliders */
    input[type=range] {
      width: 100%;
      height: 8px;
      background: #111c38;
      border: 1px solid rgba(99, 102, 241, 0.25);
      border-radius: 6px;
      outline: none;
      -webkit-appearance: none;
      cursor: pointer;
    }

    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
      cursor: pointer;
      box-shadow: 0 0 14px rgba(6, 182, 212, 0.7);
      border: 2px solid #ffffff;
      transition: transform 0.15s, box-shadow 0.15s;
    }

    input[type=range]::-webkit-slider-thumb:hover {
      transform: scale(1.25);
      box-shadow: 0 0 20px rgba(6, 182, 212, 0.9);
    }

    select#sim-state {
      width: 100%;
      padding: 10px 14px;
      border: 1px solid var(--border);
      border-radius: 8px;
      font-family: inherit;
      font-size: 0.9rem;
      background: #0d1527;
      color: #ffffff;
      outline: none;
      transition: border-color 0.2s;
    }

    select#sim-state:focus {
      border-color: var(--cyan-400);
      box-shadow: 0 0 14px var(--cyan-glow);
    }

    .sim-presets {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 22px;
    }

    .preset-chip {
      background: rgba(20, 31, 58, 0.7);
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 7px 16px;
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--text-light);
      cursor: pointer;
      transition: all 0.2s;
    }

    .preset-chip:hover {
      background: rgba(30, 48, 88, 0.9);
      border-color: var(--cyan-400);
      color: #ffffff;
      box-shadow: 0 0 14px var(--cyan-glow);
    }

    /* Output Box */
    .sim-output-box {
      background: linear-gradient(135deg, rgba(16, 26, 52, 0.95) 0%, rgba(9, 14, 28, 0.98) 100%);
      border: 1px solid rgba(16, 185, 129, 0.35);
      color: #ffffff;
      border-radius: var(--radius);
      padding: 34px 30px;
      text-align: center;
      box-shadow: var(--shadow-glass), 0 0 30px rgba(16, 185, 129, 0.2);
      position: relative;
    }

    .sim-output-title {
      font-size: 0.86rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #94a3b8;
      margin-bottom: 10px;
    }

    .sim-output-number {
      font-size: 2.9rem;
      font-weight: 800;
      font-family: var(--font-mono);
      letter-spacing: -0.03em;
      color: #34d399;
      text-shadow: 0 0 24px rgba(52, 211, 153, 0.45);
      margin-bottom: 14px;
    }

    .sim-waterfall {
      font-size: 0.82rem;
      color: #cbd5e1;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 12px 16px;
      line-height: 1.7;
      text-align: left;
    }

    /* ─── Data Tables ─── */
    .table-container {
      background: var(--bg-space-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow-glass);
      overflow-x: auto;
      margin-bottom: 24px;
      backdrop-filter: blur(16px);
    }

    .styled-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.86rem;
      text-align: left;
    }

    .styled-table th {
      background: rgba(11, 18, 36, 0.9);
      padding: 14px 18px;
      font-weight: 700;
      color: var(--cyan-400);
      border-bottom: 1px solid var(--border);
      font-size: 0.76rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .styled-table td {
      padding: 13px 18px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-light);
    }

    .styled-table tr:hover td {
      background: rgba(99, 102, 241, 0.1);
    }

    .styled-table td.mono {
      font-family: var(--font-mono);
      font-weight: 600;
    }

    /* ─── Comparison Matrix Table ─── */
    .benchmark-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
    }

    .benchmark-table th {
      background: rgba(11, 18, 36, 0.95);
      padding: 15px 18px;
      font-weight: 700;
      color: var(--cyan-400);
      border-bottom: 1px solid var(--border);
      text-align: left;
      font-size: 0.78rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .benchmark-table td {
      padding: 14px 18px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-light);
    }

    .benchmark-table tr.highlight-best td {
      background: rgba(16, 185, 129, 0.12);
      font-weight: 600;
      color: #ffffff;
      border-top: 1px solid rgba(52, 211, 153, 0.3);
      border-bottom: 1px solid rgba(52, 211, 153, 0.3);
    }

    .benchmark-table tr.highlight-best td strong {
      color: #34d399;
      text-shadow: 0 0 10px rgba(52, 211, 153, 0.4);
    }

    /* ─── Modal: Cosmic Obsidian Glass ─── */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(3, 7, 18, 0.78);
      backdrop-filter: blur(8px);
      z-index: 999;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .modal-backdrop.open {
      display: flex;
    }

    .modal-content {
      background: #0d1527;
      border: 1px solid rgba(99, 102, 241, 0.4);
      border-radius: var(--radius-lg);
      max-width: 740px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 34px;
      position: relative;
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6), 0 0 35px var(--indigo-glow);
      color: var(--text-main);
    }

    .modal-close {
      position: absolute;
      top: 20px;
      right: 20px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.12);
      width: 34px;
      height: 34px;
      border-radius: 50%;
      font-size: 1.2rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text-muted);
      transition: all 0.2s;
    }

    .modal-close:hover {
      background: rgba(255, 255, 255, 0.18);
      color: #ffffff;
      transform: scale(1.1);
    }

    .modal-step-card {
      background: rgba(20, 31, 58, 0.65);
      padding: 14px 18px;
      border-radius: 10px;
      border: 1px solid var(--border-subtle);
      border-left: 4px solid var(--indigo-400);
      color: var(--text-light);
    }

    .modal-step-card.sweet {
      border-left-color: var(--emerald-400);
      background: rgba(16, 185, 129, 0.1);
    }

    /* ─── Footer ─── */
    footer {
      text-align: center;
      font-size: 0.84rem;
      color: var(--text-muted);
      margin-top: 50px;
      padding-top: 24px;
      border-top: 1px solid var(--border-subtle);
    }
  </style>
</head>
<body>

<div class="container">

  <!-- Breadcrumb -->
  <nav class="breadcrumb">
    <a href="#home">
      <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
      </svg>
      Home
    </a>
    <span class="sep">&gt;</span>
    <span>Regression Analysis</span>
    <span class="sep">&gt;</span>
    <span class="current">50 Startups Feature Progression</span>
  </nav>

  <!-- Top Title Header -->
  <div class="top-header">
    <div class="title-group">
      <div class="title-icon">
        <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
        </svg>
      </div>
      <h1 class="main-title">50 Startups Multiple Linear Regression Explorer</h1>
      <span class="badge-crisp" onclick="openCrispModal()" title="View CRISP-DM Methodology & Details">CRISP-DM</span>
    </div>
    <div class="header-actions">
      <button class="btn-outline" onclick="openCrispModal()">
        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
        </svg>
        CRISP-DM Reference
      </button>
    </div>
  </div>

  <!-- Hero Banner (Feature Selection & Parsimony Analysis) -->
  <div class="hero-card">
    <h2 class="hero-title">Feature Selection &amp; Parsimony Analysis</h2>
    <p class="hero-desc">
      Compare 5 Machine Learning Feature Selection Algorithms (Lasso, Forward SFS, RFE, ElasticNet, Exhaustive Search) against Baseline OLS. Explore the bias-variance tradeoff across feature counts <code>k = 1 ... 5</code>, pinpointing the <strong>2-feature optimal sweet spot</strong> and the <strong>5-feature overfitting cliff</strong>.
    </p>
    <div class="hero-badges">
      <div class="hero-badge">
        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"/>
        </svg>
        50 Startups Dataset
      </div>
      <div class="hero-badge">
        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
        </svg>
        5 Selection Methods
      </div>
      <div class="hero-badge highlight-sweet">
        ★ Global Sweet Spot: k=2 ($8,198.80 RMSE)
      </div>
      <div class="hero-badge highlight-cliff">
        ▲ Overfitting Warning: k=5 ($9,137.99 RMSE)
      </div>
    </div>
  </div>

  <!-- Section 1: Algorithm Selector -->
  <div class="control-card">
    <div class="section-label">
      <span>≡</span> 1. SELECT FEATURE SELECTION ALGORITHM
    </div>
    <div class="pill-group" id="algo-pill-group">
      <button class="btn-pill selected-algo" data-algo="lasso" onclick="selectAlgo('lasso')">
        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/></svg>
        Lasso (L1 Ranking)
        <span class="sub-tag">Matches Benchmark</span>
      </button>

      <button class="btn-pill" data-algo="forward_sfs" onclick="selectAlgo('forward_sfs')">
        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11l5-5m0 0l5 5m-5-5v12"/></svg>
        Forward SFS
        <span class="sub-tag">Greedy</span>
      </button>

      <button class="btn-pill" data-algo="rfe" onclick="selectAlgo('rfe')">
        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.121 14.121L19 19m-7-7l7-7m-7 7l-2.879 2.879M12 12L9.121 9.121m0 5.758a3 3 0 10-4.243 4.243 3 3 0 004.243-4.243zm0-5.758a3 3 0 10-4.243-4.243 3 3 0 004.243 4.243z"/></svg>
        RFE
        <span class="sub-tag">Backward</span>
      </button>

      <button class="btn-pill" data-algo="elasticnet" onclick="selectAlgo('elasticnet')">
        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        ElasticNet
        <span class="sub-tag">L1 + L2</span>
      </button>

      <button class="btn-pill" data-algo="exhaustive" onclick="selectAlgo('exhaustive')">
        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        Exhaustive Search
        <span class="sub-tag">Best Subset</span>
      </button>

      <button class="btn-pill compare-btn" id="btn-toggle-compare" onclick="toggleCompareMode()">
        ★ Compare All 5 Methods
      </button>
    </div>
  </div>

  <!-- Section 2: Number of Features (k = 1 to 5) -->
  <div class="control-card">
    <div class="section-label">
      <span>≡</span> 2. NUMBER OF FEATURES (K = 1 TO 5)
    </div>
    <div class="pill-group" id="k-pill-group">
      <button class="btn-pill" data-k="1" onclick="selectK(1)">
        k = 1 <span class="sub-tag" id="k1-tag">(R&amp;D Spend)</span>
      </button>

      <button class="btn-pill selected-k-sweet" data-k="2" onclick="selectK(2)">
        k = 2 ★ Optimal Sweet Spot (Min RMSE)
      </button>

      <button class="btn-pill" data-k="3" onclick="selectK(3)">
        k = 3 <span class="sub-tag" id="k3-tag">(+ State / Admin)</span>
      </button>

      <button class="btn-pill" data-k="4" onclick="selectK(4)">
        k = 4 <span class="sub-tag" id="k4-tag">(4 Predictors)</span>
      </button>

      <button class="btn-pill" data-k="5" onclick="selectK(5)">
        k = 5 ▲ Full Model (Overfitting Cliff)
      </button>
    </div>
  </div>

  <!-- Key Metric Cards Row (Row of 5 Cards) -->
  <div class="metrics-grid">
    <!-- Card 1: TEST RMSE -->
    <div class="metric-card">
      <div class="metric-header">
        <span class="metric-label">TEST RMSE</span>
        <span class="metric-pill pill-green" id="card-rmse-pill">
          OPTIMAL SWEET SPOT
        </span>
      </div>
      <div class="metric-value" id="val-rmse">$8,198.80</div>
      <div class="metric-desc" id="desc-rmse">Lower is better (Best across methods)</div>
    </div>

    <!-- Card 2: R² SCORE -->
    <div class="metric-card">
      <div class="metric-header">
        <span class="metric-label">R² SCORE</span>
        <span class="metric-pill pill-blue" id="card-r2-pill">
          94.7% FIT
        </span>
      </div>
      <div class="metric-value" id="val-r2">0.9474</div>
      <div class="metric-desc" id="desc-r2">Explains 94.74% of profit variance</div>
    </div>

    <!-- Card 3: ADJUSTED R² -->
    <div class="metric-card">
      <div class="metric-header">
        <span class="metric-label">ADJUSTED R²</span>
        <span class="metric-icon-small" title="Penalizes non-informative parameters">⚖️</span>
      </div>
      <div class="metric-value" id="val-adj-r2">0.9324</div>
      <div class="metric-desc">Penalizes redundant parameters</div>
    </div>

    <!-- Card 4: MEAN ABSOLUTE ERROR -->
    <div class="metric-card">
      <div class="metric-header">
        <span class="metric-label">MEAN ABSOLUTE ERROR</span>
        <span class="metric-icon-small" title="Average dollar error per startup">📋</span>
      </div>
      <div class="metric-value" id="val-mae">$6,886.59</div>
      <div class="metric-desc">Average prediction error ($)</div>
    </div>

    <!-- Card 5: F-STATISTIC -->
    <div class="metric-card">
      <div class="metric-header">
        <span class="metric-label">F-STATISTIC</span>
        <span class="metric-pill pill-green">P &lt; 0.0001</span>
      </div>
      <div class="metric-value" id="val-f">349.0</div>
      <div class="metric-desc">Model is highly statistically significant</div>
    </div>
  </div>

  <!-- Summary Status Bar -->
  <div class="summary-bar">
    <div class="active-predictors">
      <span class="active-predictors-title">
        <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="color:var(--emerald-400)">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
        </svg>
        Active Predictors (<span id="active-feature-count">2</span>):
      </span>
      <div id="active-feature-chips" style="display:inline-flex;gap:8px;flex-wrap:wrap;">
        <span class="feature-tag">R&amp;D Spend</span>
        <span class="feature-tag">Marketing Spend</span>
      </div>
    </div>
    <div class="occam-badge" id="occam-badge-text">
      ★ Occam's Razor: 2 features yield the minimum test RMSE ($8,198.80) and peak R² (0.9474).
    </div>
  </div>

  <!-- Tabbed Explorer Section -->
  <div class="section-tabs-nav">
    <button class="tab-btn active" onclick="switchTab('charts')">
      📈 Performance &amp; Bias-Variance Curves
    </button>
    <button class="tab-btn" onclick="switchTab('comparison')">
      ⚡ Compare All 5 Methods
    </button>
    <button class="tab-btn" onclick="switchTab('simulator')">
      🎛️ Live What-If Simulator
    </button>
    <button class="tab-btn" onclick="switchTab('residuals')">
      🎯 Actual vs. Predicted &amp; Residuals
    </button>
    <button class="tab-btn" onclick="switchTab('dataset')">
      📊 50 Startups Dataset
    </button>
  </div>

  <!-- TAB 1: CHARTS -->
  <div class="tab-pane active" id="tab-charts">
    <div class="chart-grid-2">
      <!-- Chart 1: Test RMSE Curve -->
      <div class="chart-card">
        <div class="chart-header">
          <div>
            <div class="chart-title">Test RMSE Progression (Parsimony Curve)</div>
            <div class="chart-subtitle">Bias-Variance Tradeoff: Drops to Sweet Spot (k=2), then rises into Overfitting (k=5)</div>
          </div>
        </div>
        <div class="canvas-wrapper">
          <canvas id="chart-rmse"></canvas>
        </div>
      </div>

      <!-- Chart 2: R2 and Adj R2 -->
      <div class="chart-card">
        <div class="chart-header">
          <div>
            <div class="chart-title">R² vs. Adjusted R² Penalty</div>
            <div class="chart-subtitle">Adjusted R² strictly decreases after k=2 as degrees of freedom are lost</div>
          </div>
        </div>
        <div class="canvas-wrapper">
          <canvas id="chart-r2"></canvas>
        </div>
      </div>
    </div>

    <!-- Model Fitted Equation Card -->
    <div class="chart-card" style="margin-bottom:24px;">
      <div class="chart-header">
        <div>
          <div class="chart-title">Fitted Regression Equation for Selected Model</div>
          <div class="chart-subtitle">Ordinary Least Squares coefficients fitted on training set (N=40, random_state=0)</div>
        </div>
      </div>
      <div class="equation-box" id="model-equation-str">
        Profit = $46,346.34 + 0.7886 * (R&amp;D Spend) + 0.0326 * (Marketing Spend)
      </div>
    </div>
  </div>

  <!-- TAB 2: MULTI-METHOD COMPARISON -->
  <div class="tab-pane" id="tab-comparison">
    <div class="chart-card" style="margin-bottom:20px;">
      <div class="chart-header">
        <div>
          <div class="chart-title">5 Machine Learning Methods Overlay (Test RMSE across k)</div>
          <div class="chart-subtitle">Lasso (L1), Forward SFS, RFE, ElasticNet, and Exhaustive Search</div>
        </div>
      </div>
      <div class="canvas-wrapper" style="height:340px;">
        <canvas id="chart-multi-methods"></canvas>
      </div>
    </div>

    <div class="table-container">
      <table class="benchmark-table">
        <thead>
          <tr>
            <th>Algorithm</th>
            <th>k=1 RMSE</th>
            <th>k=2 RMSE (Sweet Spot)</th>
            <th>k=3 RMSE</th>
            <th>k=4 RMSE</th>
            <th>k=5 RMSE (Full)</th>
            <th>Optimal k</th>
            <th>Best Test RMSE</th>
          </tr>
        </thead>
        <tbody id="benchmark-table-body">
          <!-- Populated by JS -->
        </tbody>
      </table>
    </div>
  </div>

  <!-- TAB 3: WHAT-IF SIMULATOR -->
  <div class="tab-pane" id="tab-simulator">
    <div class="sim-card">
      <div class="sim-grid">
        <!-- Sliders -->
        <div>
          <h3 style="font-family:var(--font-heading);font-size:1.25rem;font-weight:700;margin-bottom:20px;color:#ffffff;">
            Interactive Profit Predictor
          </h3>

          <div class="sim-slider-row">
            <div class="sim-slider-label-row">
              <span>🔬 R&amp;D Spend</span>
              <span class="sim-slider-val" id="disp-rd">$100,000</span>
            </div>
            <input type="range" id="sim-rd" min="0" max="200000" step="1000" value="100000" oninput="runSimulation()" />
          </div>

          <div class="sim-slider-row">
            <div class="sim-slider-label-row">
              <span>📢 Marketing Spend</span>
              <span class="sim-slider-val" id="disp-mkt">$200,000</span>
            </div>
            <input type="range" id="sim-mkt" min="0" max="500000" step="2500" value="200000" oninput="runSimulation()" />
          </div>

          <div class="sim-slider-row">
            <div class="sim-slider-label-row">
              <span>🏢 Administration Spend</span>
              <span class="sim-slider-val" id="disp-adm">$120,000</span>
            </div>
            <input type="range" id="sim-adm" min="40000" max="200000" step="1000" value="120000" oninput="runSimulation()" />
          </div>

          <div class="sim-slider-row">
            <div class="sim-slider-label-row">
              <span>📍 Startup State / Headquarters</span>
              <span class="sim-slider-val" id="disp-state">California</span>
            </div>
            <select id="sim-state" onchange="runSimulation()">
              <option value="California">California (Reference Category / Baseline)</option>
              <option value="New York">New York</option>
              <option value="Florida">Florida</option>
            </select>
          </div>

          <div class="sim-presets">
            <span style="font-size:0.8rem;font-weight:600;color:var(--text-muted);">Quick Presets:</span>
            <button class="preset-chip" onclick="applyPreset(160000, 400000, 130000, 'California')">🚀 Unicorn Tech Expansion</button>
            <button class="preset-chip" onclick="applyPreset(110000, 200000, 120000, 'New York')">⚖️ Industry Benchmark</button>
            <button class="preset-chip" onclick="applyPreset(25000, 75000, 60000, 'Florida')">🌱 Lean Bootstrapped</button>
          </div>
        </div>

        <!-- Result Box -->
        <div class="sim-output-box">
          <div class="sim-output-title">Estimated Annual Profit</div>
          <div class="sim-output-number" id="sim-profit-result">$131,720</div>
          <div class="sim-waterfall" id="sim-waterfall-breakdown">
            <!-- Dynamic waterfall explanation -->
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 4: ACTUAL VS PREDICTED & RESIDUALS -->
  <div class="tab-pane" id="tab-residuals">
    <div class="chart-card" style="margin-bottom:24px;">
      <div class="chart-header">
        <div>
          <div class="chart-title">Actual vs. Predicted Profit (Held-out Test Set, N=10)</div>
          <div class="chart-subtitle">Dotted line represents perfect prediction (y = ŷ). Closer points indicate higher precision.</div>
        </div>
      </div>
      <div class="canvas-wrapper" style="height:320px;">
        <canvas id="chart-actual-pred"></canvas>
      </div>
    </div>

    <div class="table-container">
      <table class="styled-table">
        <thead>
          <tr>
            <th>Startup #</th>
            <th>R&amp;D Spend</th>
            <th>Admin</th>
            <th>Marketing</th>
            <th>State</th>
            <th>Actual Profit</th>
            <th>Predicted Profit</th>
            <th>Residual (Error)</th>
            <th>Absolute Error</th>
            <th>% Error</th>
          </tr>
        </thead>
        <tbody id="test-residuals-tbody">
          <!-- Populated by JS -->
        </tbody>
      </table>
    </div>
  </div>

  <!-- TAB 5: 50 STARTUPS RAW DATASET -->
  <div class="tab-pane" id="tab-dataset">
    <div class="chart-card" style="margin-bottom:16px;">
      <div class="chart-header">
        <div>
          <div class="chart-title">50 Startups Complete Dataset</div>
          <div class="chart-subtitle">50 venture-backed companies across New York, California, and Florida</div>
        </div>
        <div>
          <input type="text" id="dataset-search" placeholder="Search startups or state..." oninput="filterDatasetTable()" style="padding:8px 16px;background:#0d1527;border:1px solid var(--border);border-radius:8px;font-size:0.86rem;color:#ffffff;outline:none;" />
        </div>
      </div>
    </div>

    <div class="table-container">
      <table class="styled-table" id="raw-dataset-table">
        <thead>
          <tr>
            <th>Row</th>
            <th>R&amp;D Spend</th>
            <th>Administration</th>
            <th>Marketing Spend</th>
            <th>State</th>
            <th>Profit</th>
            <th>Split Partition</th>
          </tr>
        </thead>
        <tbody id="dataset-tbody">
          <!-- Populated by JS -->
        </tbody>
      </table>
    </div>
  </div>

  <!-- Footer -->
  <footer>
    <p>50 Startups Multiple Linear Regression Explorer · CRISP-DM Feature Selection SOP &amp; Parsimony Analysis</p>
    <p style="margin-top:6px;font-size:0.78rem;color:var(--text-dim);">Scikit-Learn Standard Random State (0) Alignment · All 5 Algorithms Verified</p>
  </footer>

</div>

<!-- CRISP-DM & Methodology Modal -->
<div class="modal-backdrop" id="crisp-modal" onclick="closeCrispModal(event)">
  <div class="modal-content" onclick="event.stopPropagation()">
    <button class="modal-close" onclick="closeCrispModal()">&times;</button>
    <h2 style="font-family:var(--font-heading);font-size:1.45rem;font-weight:800;color:#ffffff;margin-bottom:14px;">
      CRISP-DM Machine Learning Methodology
    </h2>
    <p style="color:var(--text-muted);font-size:0.92rem;margin-bottom:20px;line-height:1.6;">
      Cross-Industry Standard Process for Data Mining (CRISP-DM) provides a structured lifecycle for feature selection and regression modeling:
    </p>

    <div style="display:flex;flex-direction:column;gap:14px;font-size:0.88rem;line-height:1.65;">
      <div class="modal-step-card">
        <strong style="color:#ffffff;">1. Business Understanding:</strong> Maximize venture profit predictability while maintaining an interpretable model for executive decision-making.
      </div>
      <div class="modal-step-card">
        <strong style="color:#ffffff;">2. Data Understanding:</strong> Examine 50 records of R&amp;D, Administration, and Marketing expenditures alongside State categorical attributes.
      </div>
      <div class="modal-step-card">
        <strong style="color:#ffffff;">3. Data Preparation:</strong> One-Hot encode <code>State</code> using <code>drop_first=True</code> (California dropped as reference) to prevent the Dummy Variable Trap (multicollinearity).
      </div>
      <div class="modal-step-card">
        <strong style="color:#ffffff;">4. Modeling:</strong> Evaluate 5 feature selection algorithms across k=1 to 5 to explore model simplicity vs. explanatory capacity.
      </div>
      <div class="modal-step-card sweet">
        <strong style="color:#34d399;">5. Evaluation (Occam's Razor):</strong> Test RMSE reaches its global minimum at <strong>k=2</strong> ($8,198.80). Beyond k=2, adding Administration or State introduces parameter variance without improving test generalization, creating the <strong>overfitting cliff</strong> at k=5 ($9,137.99).
      </div>
      <div class="modal-step-card">
        <strong style="color:#ffffff;">6. Deployment:</strong> Ship static interactive dashboard with what-if simulator and automated batch prediction export.
      </div>
    </div>
  </div>
</div>

<!-- Embedded Precalculated Data -->
<script>
const MODEL_DATA = __MODEL_DATA_RAW__;

// Configure Global Chart.js Dark Mode Theme
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.07)';
Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif";

// App State
let currentAlgo = 'lasso';
let currentK = 2;
let compareMode = false;
let chartRmseInstance = null;
let chartR2Instance = null;
let chartActualPredInstance = null;
let chartMultiMethodsInstance = null;

// Currency Formatter
function formatDollar(val) {
  return '$' + Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// Select Algorithm
function selectAlgo(algo) {
  currentAlgo = algo;
  compareMode = false;
  document.getElementById('btn-toggle-compare').classList.remove('active');

  // Update button active state
  document.querySelectorAll('#algo-pill-group .btn-pill').forEach(btn => {
    if (btn.dataset.algo === algo) {
      btn.className = 'btn-pill selected-algo';
    } else if (btn.dataset.algo) {
      btn.className = 'btn-pill';
    }
  });

  updateKButtonSubtags();
  updateDashboard();
}

// Select K
function selectK(k) {
  currentK = parseInt(k, 10);
  updateKButtonStyles();
  updateDashboard();
}

// Update K buttons styling
function updateKButtonStyles() {
  document.querySelectorAll('#k-pill-group .btn-pill').forEach(btn => {
    const k = parseInt(btn.dataset.k, 10);
    if (k === currentK) {
      if (k === 2) {
        btn.className = 'btn-pill selected-k-sweet';
      } else {
        btn.className = 'btn-pill selected-k-normal';
      }
    } else {
      btn.className = 'btn-pill';
    }
  });
}

// Update sub-tags on K buttons depending on the selected algorithm's feature path
function updateKButtonSubtags() {
  const algoData = MODEL_DATA.methods[currentAlgo];
  if (!algoData) return;

  const f1 = algoData[1].features;
  const f3 = algoData[3].features;
  const f4 = algoData[4].features;

  const tag1 = document.getElementById('k1-tag');
  if (tag1) tag1.textContent = '(' + f1.join(', ') + ')';

  const tag3 = document.getElementById('k3-tag');
  if (tag3) {
    const added = f3.filter(f => !algoData[2].features.includes(f));
    tag3.textContent = added.length > 0 ? '(+ ' + added.join(', ') + ')' : '(3 Predictors)';
  }

  const tag4 = document.getElementById('k4-tag');
  if (tag4) tag4.textContent = '(4 Predictors)';
}

// Toggle Compare All Methods
function toggleCompareMode() {
  compareMode = !compareMode;
  const btn = document.getElementById('btn-toggle-compare');
  if (compareMode) {
    btn.classList.add('active');
    switchTab('comparison');
  } else {
    btn.classList.remove('active');
  }
}

// Update KPI cards, equation, summary bar, and charts
function updateDashboard() {
  const algoData = MODEL_DATA.methods[currentAlgo];
  if (!algoData) return;

  const model = algoData[currentK];
  if (!model) return;

  // 1. KPI Cards
  const valRmse = document.getElementById('val-rmse');
  const valR2 = document.getElementById('val-r2');
  const valAdjR2 = document.getElementById('val-adj-r2');
  const valMae = document.getElementById('val-mae');
  const valF = document.getElementById('val-f');

  valRmse.textContent = formatDollar(model.rmse);
  valR2.textContent = model.r2.toFixed(4);
  valAdjR2.textContent = model.adj_r2.toFixed(4);
  valMae.textContent = formatDollar(model.mae);
  valF.textContent = model.f_stat.toFixed(1);

  // RMSE card badge & description
  const rmsePill = document.getElementById('card-rmse-pill');
  const rmseDesc = document.getElementById('desc-rmse');
  if (currentK === 2) {
    rmsePill.className = 'metric-pill pill-green';
    rmsePill.textContent = 'OPTIMAL SWEET SPOT';
    rmseDesc.textContent = 'Lower is better (Best across methods)';
  } else if (currentK === 5) {
    rmsePill.className = 'metric-pill pill-amber';
    rmsePill.textContent = 'OVERFITTING WARNING';
    rmseDesc.textContent = '+$939.19 RMSE penalty vs. k=2';
  } else {
    rmsePill.className = 'metric-pill pill-blue';
    rmsePill.textContent = 'k = ' + currentK;
    rmseDesc.textContent = 'Test Evaluation RMSE';
  }

  // R2 card badge
  const r2Pill = document.getElementById('card-r2-pill');
  const r2Pct = (model.r2 * 100).toFixed(1) + '% FIT';
  r2Pill.textContent = r2Pct;
  document.getElementById('desc-r2').textContent = `Explains ${(model.r2 * 100).toFixed(2)}% of profit variance`;

  // 2. Active features chips
  document.getElementById('active-feature-count').textContent = model.features.length;
  const chipContainer = document.getElementById('active-feature-chips');
  chipContainer.innerHTML = '';
  model.features.forEach(f => {
    const chip = document.createElement('span');
    chip.className = 'feature-tag';
    chip.textContent = f;
    chipContainer.appendChild(chip);
  });

  // 3. Occam's Razor badge text
  const occamBadge = document.getElementById('occam-badge-text');
  if (currentK === 2) {
    occamBadge.textContent = "★ Occam's Razor: 2 features yield the minimum test RMSE ($8,198.80) and peak R² (0.9474).";
    occamBadge.className = 'occam-badge';
    occamBadge.style.background = 'rgba(16, 185, 129, 0.14)';
    occamBadge.style.color = '#6ee7b7';
    occamBadge.style.borderColor = 'rgba(52, 211, 153, 0.4)';
  } else if (currentK === 1) {
    occamBadge.textContent = "Underfitting: 1 feature under-specifies marketing interaction (RMSE: $8,274.87).";
    occamBadge.className = 'occam-badge';
    occamBadge.style.background = 'rgba(6, 182, 212, 0.14)';
    occamBadge.style.color = '#38bdf8';
    occamBadge.style.borderColor = 'rgba(56, 189, 248, 0.4)';
  } else if (currentK >= 3 && currentK < 5) {
    occamBadge.textContent = `Parameter Penalty: Adding ${currentK} features increases variance (RMSE: ${formatDollar(model.rmse)}).`;
    occamBadge.className = 'occam-badge';
    occamBadge.style.background = 'rgba(245, 158, 11, 0.14)';
    occamBadge.style.color = '#fbbf24';
    occamBadge.style.borderColor = 'rgba(251, 191, 36, 0.4)';
  } else {
    occamBadge.textContent = "Overfitting Cliff: 5 features maximize parameters but degrade test RMSE to $9,137.99.";
    occamBadge.className = 'occam-badge';
    occamBadge.style.background = 'rgba(244, 63, 94, 0.14)';
    occamBadge.style.color = '#fb7185';
    occamBadge.style.borderColor = 'rgba(251, 113, 133, 0.4)';
  }

  // 4. Equation Callout
  const eqTerms = Object.entries(model.coef).map(([feat, coef]) => {
    const sign = coef >= 0 ? '+' : '-';
    return `${sign} ${Math.abs(coef).toFixed(4)} * (${feat})`;
  });
  const eqStr = `Profit = $${model.intercept.toLocaleString('en-US', { minimumFractionDigits: 2 })} ${eqTerms.join(' ')}`;
  document.getElementById('model-equation-str').textContent = eqStr;

  // 5. Update Charts
  renderCharts();

  // 6. Update Test Residuals Table
  renderTestResiduals(model.test_predictions);

  // 7. Update Simulator
  runSimulation();
}

// Render Charts
function renderCharts() {
  const algoData = MODEL_DATA.methods[currentAlgo];
  if (!algoData) return;

  const ks = [1, 2, 3, 4, 5];
  const rmseValues = ks.map(k => algoData[k].rmse);
  const r2Values = ks.map(k => algoData[k].r2);
  const adjR2Values = ks.map(k => algoData[k].adj_r2);

  // Chart 1: RMSE Curve
  const ctxRmse = document.getElementById('chart-rmse');
  if (ctxRmse) {
    if (chartRmseInstance) chartRmseInstance.destroy();

    const pointColors = ks.map(k => {
      if (k === currentK) return '#818cf8';
      if (k === 2) return '#34d399';
      if (k === 5) return '#fbbf24';
      return '#64748b';
    });
    const pointRadii = ks.map(k => (k === currentK ? 9 : 5));

    chartRmseInstance = new Chart(ctxRmse, {
      type: 'line',
      data: {
        labels: ['k=1 (R&D)', 'k=2 (Sweet Spot)', 'k=3', 'k=4', 'k=5 (Full Model)'],
        datasets: [{
          label: 'Test Set RMSE ($)',
          data: rmseValues,
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99, 102, 241, 0.12)',
          fill: true,
          tension: 0.35,
          pointBackgroundColor: pointColors,
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: pointRadii
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(13, 21, 39, 0.95)',
            titleColor: '#ffffff',
            bodyColor: '#38bdf8',
            borderColor: 'rgba(99, 102, 241, 0.4)',
            borderWidth: 1,
            callbacks: {
              label: (ctx) => `RMSE: ${formatDollar(ctx.raw)}`
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            title: { display: true, text: 'Test RMSE ($)', color: '#94a3b8' },
            min: Math.min(...rmseValues) * 0.95,
            max: Math.max(...rmseValues) * 1.05
          }
        }
      }
    });
  }

  // Chart 2: R2 and Adj R2
  const ctxR2 = document.getElementById('chart-r2');
  if (ctxR2) {
    if (chartR2Instance) chartR2Instance.destroy();
    chartR2Instance = new Chart(ctxR2, {
      type: 'line',
      data: {
        labels: ['k=1', 'k=2', 'k=3', 'k=4', 'k=5'],
        datasets: [
          {
            label: 'Test R²',
            data: r2Values,
            borderColor: '#38bdf8',
            backgroundColor: 'transparent',
            tension: 0.3,
            borderWidth: 2.5,
            pointRadius: 5,
            pointBackgroundColor: '#38bdf8'
          },
          {
            label: 'Adjusted R²',
            data: adjR2Values,
            borderColor: '#fbbf24',
            backgroundColor: 'transparent',
            borderDash: [5, 5],
            tension: 0.3,
            borderWidth: 2.5,
            pointRadius: 5,
            pointBackgroundColor: '#fbbf24'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { 
            position: 'top',
            labels: { color: '#cbd5e1' }
          },
          tooltip: {
            backgroundColor: 'rgba(13, 21, 39, 0.95)',
            titleColor: '#ffffff',
            borderColor: 'rgba(99, 102, 241, 0.4)',
            borderWidth: 1,
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toFixed(4)}`
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            title: { display: true, text: 'Score', color: '#94a3b8' },
            min: 0.85,
            max: 0.98
          }
        }
      }
    });
  }

  // Chart 3: Actual vs Predicted Scatter
  const currentModel = algoData[currentK];
  const ctxActualPred = document.getElementById('chart-actual-pred');
  if (ctxActualPred && currentModel) {
    if (chartActualPredInstance) chartActualPredInstance.destroy();

    const scatterData = currentModel.test_predictions.map(p => ({
      x: p.actual,
      y: p.predicted,
      residual: p.residual,
      startup: p.idx
    }));

    const minVal = 60000;
    const maxVal = 200000;

    chartActualPredInstance = new Chart(ctxActualPred, {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: 'Startups (Held-out Test Set)',
            data: scatterData,
            backgroundColor: '#818cf8',
            borderColor: '#ffffff',
            borderWidth: 2,
            pointRadius: 7,
            pointHoverRadius: 10
          },
          {
            label: 'Ideal 45° Line (y = ŷ)',
            type: 'line',
            data: [{ x: minVal, y: minVal }, { x: maxVal, y: maxVal }],
            borderColor: 'rgba(148, 163, 184, 0.45)',
            borderDash: [6, 6],
            fill: false,
            pointRadius: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: '#cbd5e1' }
          },
          tooltip: {
            backgroundColor: 'rgba(13, 21, 39, 0.95)',
            titleColor: '#ffffff',
            borderColor: 'rgba(99, 102, 241, 0.4)',
            borderWidth: 1,
            callbacks: {
              label: (ctx) => {
                if (ctx.datasetIndex === 1) return 'Perfect Fit Line';
                const d = ctx.raw;
                return `Startup #${d.startup}: Actual ${formatDollar(d.x)}, Pred ${formatDollar(d.y)} (Res: ${formatDollar(d.residual)})`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            title: { display: true, text: 'Actual Profit ($)', color: '#94a3b8' },
            min: minVal,
            max: maxVal
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            title: { display: true, text: 'Predicted Profit ($)', color: '#94a3b8' },
            min: minVal,
            max: maxVal
          }
        }
      }
    });
  }

  // Chart 4: Multi-Method Comparison
  renderMultiMethodChart();
}

// Multi-method comparison chart and table
function renderMultiMethodChart() {
  const ctx = document.getElementById('chart-multi-methods');
  if (!ctx) return;
  if (chartMultiMethodsInstance) chartMultiMethodsInstance.destroy();

  const methods = ['lasso', 'forward_sfs', 'rfe', 'elasticnet', 'exhaustive'];
  const labels = {
    lasso: 'Lasso (L1)',
    forward_sfs: 'Forward SFS',
    rfe: 'RFE (Backward)',
    elasticnet: 'ElasticNet',
    exhaustive: 'Exhaustive Search'
  };
  const colors = {
    lasso: '#818cf8',
    forward_sfs: '#34d399',
    rfe: '#fb7185',
    elasticnet: '#fbbf24',
    exhaustive: '#c084fc'
  };

  const datasets = methods.map(m => {
    const vals = [1, 2, 3, 4, 5].map(k => MODEL_DATA.methods[m][k].rmse);
    return {
      label: labels[m],
      data: vals,
      borderColor: colors[m],
      backgroundColor: 'transparent',
      tension: 0.25,
      borderWidth: 2.5,
      pointRadius: 4,
      pointBackgroundColor: colors[m]
    };
  });

  chartMultiMethodsInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['k=1', 'k=2', 'k=3', 'k=4', 'k=5'],
      datasets: datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { 
          position: 'top',
          labels: { color: '#cbd5e1' }
        },
        tooltip: {
          backgroundColor: 'rgba(13, 21, 39, 0.95)',
          titleColor: '#ffffff',
          borderColor: 'rgba(99, 102, 241, 0.4)',
          borderWidth: 1,
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${formatDollar(ctx.raw)}`
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        y: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          title: { display: true, text: 'Test RMSE ($)', color: '#94a3b8' },
          min: 7500,
          max: 42000
        }
      }
    }
  });

  // Populate comparison table
  const tbody = document.getElementById('benchmark-table-body');
  if (tbody) {
    tbody.innerHTML = '';
    methods.forEach(m => {
      const data = MODEL_DATA.methods[m];
      const tr = document.createElement('tr');
      if (m === 'lasso' || m === 'forward_sfs' || m === 'exhaustive') {
        tr.className = 'highlight-best';
      }
      tr.innerHTML = `
        <td><strong>${labels[m]}</strong></td>
        <td>${formatDollar(data[1].rmse)}</td>
        <td><strong>${formatDollar(data[2].rmse)}</strong></td>
        <td>${formatDollar(data[3].rmse)}</td>
        <td>${formatDollar(data[4].rmse)}</td>
        <td>${formatDollar(data[5].rmse)}</td>
        <td><span class="metric-pill pill-green">k=2</span></td>
        <td><strong style="color:#34d399;">${formatDollar(data[2].rmse)}</strong></td>
      `;
      tbody.appendChild(tr);
    });
  }
}

// Render Test Set Residuals Table
function renderTestResiduals(predictions) {
  const tbody = document.getElementById('test-residuals-tbody');
  if (!tbody || !predictions) return;
  tbody.innerHTML = '';

  predictions.forEach(p => {
    const tr = document.createElement('tr');
    const resColor = p.residual >= 0 ? '#34d399' : '#fb7185';
    tr.innerHTML = `
      <td class="mono" style="color:var(--cyan-400);">#${p.idx}</td>
      <td class="mono">${formatDollar(p.rd)}</td>
      <td class="mono">${formatDollar(p.adm)}</td>
      <td class="mono">${formatDollar(p.mkt)}</td>
      <td><span class="feature-tag" style="background:rgba(255,255,255,0.06);color:#cbd5e1;border-color:rgba(255,255,255,0.12);">${p.state}</span></td>
      <td class="mono"><strong>${formatDollar(p.actual)}</strong></td>
      <td class="mono" style="color:#818cf8;font-weight:700;">${formatDollar(p.predicted)}</td>
      <td class="mono" style="color:${resColor};font-weight:700;">${p.residual >= 0 ? '+' : ''}${formatDollar(p.residual)}</td>
      <td class="mono">${formatDollar(p.abs_error)}</td>
      <td class="mono">${p.pct_error.toFixed(2)}%</td>
    `;
    tbody.appendChild(tr);
  });
}

// Render Complete 50 Startups Dataset
function renderDatasetTable() {
  const tbody = document.getElementById('dataset-tbody');
  if (!tbody || !MODEL_DATA.dataset) return;
  tbody.innerHTML = '';

  MODEL_DATA.dataset.forEach((row, i) => {
    const isTest = MODEL_DATA.test_indices.includes(i);
    const tr = document.createElement('tr');
    tr.dataset.text = `${row.State} ${row.Profit}`.toLowerCase();
    tr.innerHTML = `
      <td class="mono" style="color:var(--cyan-400);">#${i}</td>
      <td class="mono">${formatDollar(row['R&D Spend'])}</td>
      <td class="mono">${formatDollar(row['Administration'])}</td>
      <td class="mono">${formatDollar(row['Marketing Spend'])}</td>
      <td>${row.State}</td>
      <td class="mono"><strong>${formatDollar(row.Profit)}</strong></td>
      <td>
        ${isTest ? '<span class="metric-pill pill-amber">Held-out Test (20%)</span>' : '<span class="metric-pill pill-blue">Train Set (80%)</span>'}
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// Filter dataset table
function filterDatasetTable() {
  const q = document.getElementById('dataset-search').value.toLowerCase();
  document.querySelectorAll('#dataset-tbody tr').forEach(tr => {
    tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
}

// Interactive Simulator
function runSimulation() {
  const rd = parseFloat(document.getElementById('sim-rd').value);
  const mkt = parseFloat(document.getElementById('sim-mkt').value);
  const adm = parseFloat(document.getElementById('sim-adm').value);
  const state = document.getElementById('sim-state').value;

  document.getElementById('disp-rd').textContent = formatDollar(rd);
  document.getElementById('disp-mkt').textContent = formatDollar(mkt);
  document.getElementById('disp-adm').textContent = formatDollar(adm);
  document.getElementById('disp-state').textContent = state;

  const algoData = MODEL_DATA.methods[currentAlgo];
  if (!algoData) return;
  const model = algoData[currentK];
  if (!model) return;

  let profit = model.intercept;
  let breakdown = [`Base Intercept: <strong style="color:#ffffff;">${formatDollar(model.intercept)}</strong>`];

  if (model.coef['R&D Spend']) {
    const term = model.coef['R&D Spend'] * rd;
    profit += term;
    breakdown.push(`+ R&D Spend (${model.coef['R&D Spend'].toFixed(4)} × ${formatDollar(rd)}) = <span style="color:#34d399;">${formatDollar(term)}</span>`);
  }
  if (model.coef['Marketing Spend']) {
    const term = model.coef['Marketing Spend'] * mkt;
    profit += term;
    breakdown.push(`+ Marketing Spend (${model.coef['Marketing Spend'].toFixed(4)} × ${formatDollar(mkt)}) = <span style="color:#34d399;">${formatDollar(term)}</span>`);
  }
  if (model.coef['Administration']) {
    const term = model.coef['Administration'] * adm;
    profit += term;
    breakdown.push(`+ Administration (${model.coef['Administration'].toFixed(4)} × ${formatDollar(adm)}) = <span style="color:#38bdf8;">${formatDollar(term)}</span>`);
  }
  if (state === 'Florida' && model.coef['State_Florida']) {
    const term = model.coef['State_Florida'];
    profit += term;
    breakdown.push(`+ Florida adjustment = <span style="color:#fbbf24;">${formatDollar(term)}</span>`);
  }
  if (state === 'New York' && model.coef['State_New York']) {
    const term = model.coef['State_New York'];
    profit += term;
    breakdown.push(`+ New York adjustment = <span style="color:#fbbf24;">${formatDollar(term)}</span>`);
  }

  document.getElementById('sim-profit-result').textContent = formatDollar(profit);
  document.getElementById('sim-waterfall-breakdown').innerHTML = breakdown.join('<br>');
}

// Preset Applier
function applyPreset(rd, mkt, adm, state) {
  document.getElementById('sim-rd').value = rd;
  document.getElementById('sim-mkt').value = mkt;
  document.getElementById('sim-adm').value = adm;
  document.getElementById('sim-state').value = state;
  runSimulation();
}

// Tab Switcher
function switchTab(tabId) {
  document.querySelectorAll('.section-tabs-nav .tab-btn').forEach((btn, idx) => {
    btn.classList.toggle('active', btn.getAttribute('onclick').includes(tabId));
  });
  document.querySelectorAll('.tab-pane').forEach(pane => {
    pane.classList.remove('active');
  });
  const target = document.getElementById('tab-' + tabId);
  if (target) target.classList.add('active');

  // Re-render chart if switching to charts or comparison
  if (tabId === 'charts' || tabId === 'comparison' || tabId === 'residuals') {
    setTimeout(() => {
      renderCharts();
    }, 50);
  }
}

// Modal functions
function openCrispModal() {
  document.getElementById('crisp-modal').classList.add('open');
}
function closeCrispModal(e) {
  document.getElementById('crisp-modal').classList.remove('open');
}

// Initialize on DOM load
window.addEventListener('DOMContentLoaded', () => {
  updateKButtonSubtags();
  updateKButtonStyles();
  updateDashboard();
  renderDatasetTable();
});
</script>

</body>
</html>
"""

# Replace __MODEL_DATA_RAW__ with JSON string
final_html = html_template.replace("__MODEL_DATA_RAW__", model_data_raw)

with open("forward_selection.html", "w", encoding="utf-8") as f:
    f.write(final_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Generated forward_selection.html and index.html successfully with Midnight Deep Blue theme!")
