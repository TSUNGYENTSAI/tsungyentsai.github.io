#!/usr/bin/env python3
"""Publish the checked General HTML/PDF pair as local website artifacts.

Career owns resume content. This script owns only the website reading layout,
local font references, and the PDF download control. Do not edit resume.html.
"""

import argparse
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT.parent / "career/90_generated/resumes/general"

WEB_STYLE = """
<style>
  @font-face { font-family: Lato; font-style: normal; font-weight: 400; font-display: swap; src: url('assets/fonts/Lato-Regular.ttf') format('truetype'); }
  @font-face { font-family: Lato; font-style: normal; font-weight: 700; font-display: swap; src: url('assets/fonts/Lato-Bold.ttf') format('truetype'); }
  @font-face { font-family: Lato; font-style: italic; font-weight: 400; font-display: swap; src: url('assets/fonts/Lato-Italic.ttf') format('truetype'); }
  body { background: #FCFCFA; }
  .resume-toolbar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px; max-width: 794px; margin: 20px auto 0; padding: 0 16px 16px; border-bottom: 1px solid #CCD3D0; font-size: 14px; }
  .resume-toolbar a { display: inline-flex; align-items: center; min-height: 44px; color: #356B5B; text-decoration: none; }
  .resume-toolbar a:hover { text-decoration: underline; }
  .resume-toolbar a:focus-visible { outline: 2px solid #356B5B; outline-offset: 3px; }
  .resume-toolbar .download-pdf { padding: 8px 16px; border: 1px solid #A8BFB2; border-radius: 4px; background: #EFF5F2; }
  .page { max-width: calc(100% - 32px); box-shadow: none; border: 1px solid #CCD3D0; }
  @media (max-width: 760px) {
    body { font-size: 15px; line-height: 1.55; overflow-wrap: anywhere; }
    .page { width: auto; min-height: 0; margin: 20px 16px; padding: 28px 20px; }
    .topbar { grid-template-columns: 1fr; gap: 18px; }
    h1 { font-size: clamp(24px, 6vw, 34px); }
    .name-zh { font-size: 20px; margin-left: 8px; }
    .contact { min-width: 0; font-size: 13px; }
    .summary { font-size: 15px; }
    section { margin-top: 24px; }
    .section-title { font-size: 18px; margin-bottom: 12px; }
    .experience { margin-bottom: 24px; }
    .experience-head, .role-head, .education-entry { grid-template-columns: 1fr; gap: 4px; }
    .experience-title, .school { font-size: 18px; }
    .role-list, .role-item + .role-item { margin-top: 12px; }
    .role-title { font-size: 15px; }
    .experience-meta, .role-meta { white-space: normal; font-size: 13px; }
    .tech, .degree, .thesis { font-size: 13px; }
    .resume-bullets li { margin-block: 8px; }
    .compact-experience-title { flex-wrap: wrap; font-size: 15px; }
    .education-entry + .education-entry { margin-top: 18px; }
  }
  @media print {
    .resume-toolbar { display: none; }
    .page { max-width: none; border: 0; }
  }
</style>
"""

TOOLBAR = """
    <nav class="resume-toolbar" aria-label="履歷導覽" lang="zh-Hant">
      <a href="index.html">← 回到首頁</a>
      <a class="download-pdf" href="assets/resume/tsung-yen-tsai-general.pdf" download="Tsung-Yen Tsai - General.pdf">下載 PDF</a>
    </nav>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    source_html = args.source_dir / "general.html"
    source_pdf = args.source_dir / "Tsung-Yen Tsai - General.pdf"
    html = source_html.read_text()
    pdf = source_pdf.read_bytes()
    if not pdf.startswith(b"%PDF") or b"%%EOF" not in pdf[-1024:]:
        raise ValueError("Source PDF is incomplete")
    if html.count("</head>") != 1 or html.count("<body>") != 1:
        raise ValueError("Unexpected General HTML structure")
    html = re.sub(r"\s*@import url\('https://fonts\.googleapis\.com/[^']+'\);", "", html)
    html = html.replace("</head>", WEB_STYLE + "</head>", 1)
    html = html.replace("<body>", "<body>" + TOOLBAR, 1)
    html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"
    pdf_target = ROOT / "assets/resume/tsung-yen-tsai-general.pdf"
    pdf_target.parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "resume.html").write_text(html)
    shutil.copyfile(source_pdf, pdf_target)
    print("Synced resume.html and the unchanged General PDF download.")


if __name__ == "__main__":
    main()
