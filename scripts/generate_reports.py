"""
DevOps Lab 1 - Report Generator
Student: Kartik | Roll No.: 2301730205 | Email: kartikjangra5366@gmail.com
Generates all 7 PDF practical reports.
"""

import os
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, PageBreak,
    Preformatted
)
from reportlab.platypus import Image as RLImage
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SS_DIR = os.path.join(BASE, "docs", "screenshots")
RPT_DIR= os.path.join(BASE, "reports")
os.makedirs(RPT_DIR, exist_ok=True)

# ─── Fonts ────────────────────────────────────────────────────────────────────
FONT_DIR = os.path.join(BASE, "docs", "fonts")

def try_register(name, path):
    full = os.path.join(FONT_DIR, path)
    if os.path.exists(full):
        pdfmetrics.registerFont(TTFont(name, full))
        return True
    return False

HAS_UBUNTU = all([
    try_register("Ubuntu",         "Ubuntu-R.ttf"),
    try_register("Ubuntu-Bold",    "Ubuntu-B.ttf"),
    try_register("UbuntuMono",     "UbuntuMono-R.ttf"),
    try_register("UbuntuMono-Bold","UbuntuMono-B.ttf"),
])

BODY_FONT = "Ubuntu"       if HAS_UBUNTU else "Helvetica"
BOLD_FONT = "Ubuntu-Bold"  if HAS_UBUNTU else "Helvetica-Bold"
MONO_FONT = "UbuntuMono"   if HAS_UBUNTU else "Courier"

# ─── Page geometry ────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN_L = MARGIN_R = 2.2 * cm
MARGIN_T = 2.6 * cm
MARGIN_B = 2.2 * cm
USABLE_W = PAGE_W - MARGIN_L - MARGIN_R
HEADER_H = 42
FOOTER_H = 20

# ─── Student identity ─────────────────────────────────────────────────────────
STUDENT   = "Kartik"
ROLL      = "2301730205"
EMAIL     = "kartikjangra5366@gmail.com"
ENV       = "Ubuntu 24.04 LTS (WSL2)"
REPO_URL  = "https://github.com/Kartik/devops-lab-1"
HOSTNAME  = "KartikJangra"
COURSE    = "ENSP461 - DevOps & Automation"
LAB       = "Lab 1"

# ─── Colours ──────────────────────────────────────────────────────────────────
C_BLACK  = colors.HexColor("#000000")
C_HEADER = colors.HexColor("#1a1a2e")
C_RULE   = colors.HexColor("#2d4a7a")
C_CODE   = colors.HexColor("#f4f4f4")
C_BORDER = colors.HexColor("#aaaaaa")
C_TABLE_HEAD = colors.HexColor("#2d4a7a")
C_TABLE_ALT  = colors.HexColor("#eef2f8")

# ─── Styles ───────────────────────────────────────────────────────────────────
def get_styles():
    s = {}
    s["h1"] = ParagraphStyle("h1",
        fontName=BOLD_FONT, fontSize=13, leading=18,
        textColor=C_HEADER, spaceAfter=4, spaceBefore=10)
    s["h2"] = ParagraphStyle("h2",
        fontName=BOLD_FONT, fontSize=11, leading=15,
        textColor=C_RULE, spaceAfter=3, spaceBefore=8)
    s["body"] = ParagraphStyle("body",
        fontName=BODY_FONT, fontSize=9.5, leading=14,
        textColor=C_BLACK, spaceAfter=4, alignment=TA_JUSTIFY)
    s["bullet"] = ParagraphStyle("bullet",
        fontName=BODY_FONT, fontSize=9.5, leading=14,
        textColor=C_BLACK, spaceAfter=2,
        leftIndent=14, bulletIndent=0)
    s["caption"] = ParagraphStyle("caption",
        fontName=BOLD_FONT, fontSize=8.5, leading=12,
        textColor=C_RULE, spaceAfter=6, spaceBefore=2,
        alignment=TA_CENTER)
    s["code"] = ParagraphStyle("code",
        fontName=MONO_FONT, fontSize=8, leading=11,
        textColor=C_BLACK, spaceAfter=0,
        leftIndent=6, rightIndent=6)
    s["label"] = ParagraphStyle("label",
        fontName=BOLD_FONT, fontSize=9, leading=12,
        textColor=C_RULE, spaceAfter=2)
    s["center"] = ParagraphStyle("center",
        fontName=BODY_FONT, fontSize=9.5, leading=14,
        textColor=C_BLACK, alignment=TA_CENTER)
    s["obs"] = ParagraphStyle("obs",
        fontName=BODY_FONT, fontSize=9.5, leading=14,
        textColor=C_BLACK, spaceAfter=4, leftIndent=10,
        alignment=TA_JUSTIFY)
    return s

ST = get_styles()

# ─── Page callbacks ───────────────────────────────────────────────────────────
def make_page_callbacks(q_num, q_title):
    def header_footer(cvs, doc):
        cvs.saveState()
        # Header background
        cvs.setFillColor(C_HEADER)
        cvs.rect(0, PAGE_H - HEADER_H, PAGE_W, HEADER_H, fill=1, stroke=0)
        # Header text
        cvs.setFillColor(colors.white)
        cvs.setFont(BOLD_FONT, 10)
        cvs.drawString(MARGIN_L, PAGE_H - HEADER_H + 25,
                       f"{COURSE}  |  {LAB}: DevOps Workflow with Git & Jenkins")
        cvs.setFont(BODY_FONT, 8)
        cvs.drawString(MARGIN_L, PAGE_H - HEADER_H + 11,
                       f"Name: {STUDENT}   Roll No.: {ROLL}   Environment: {ENV}")
        # Footer rule
        cvs.setStrokeColor(C_RULE)
        cvs.setLineWidth(0.7)
        cvs.line(MARGIN_L, FOOTER_H + 6, PAGE_W - MARGIN_R, FOOTER_H + 6)
        # Footer text
        cvs.setFillColor(C_RULE)
        cvs.setFont(BODY_FONT, 8)
        cvs.drawString(MARGIN_L, FOOTER_H - 4,
                       f"Question {q_num} - {q_title}")
        cvs.setFont(BODY_FONT, 8)
        cvs.drawRightString(PAGE_W - MARGIN_R, FOOTER_H - 4,
                            f"Page {doc.page}")
        cvs.restoreState()
    return header_footer

# ─── Doc builder ──────────────────────────────────────────────────────────────
def build_doc(filename, q_num, q_title, story):
    path = os.path.join(RPT_DIR, filename)
    frame = Frame(MARGIN_L, MARGIN_B + FOOTER_H,
                  USABLE_W, PAGE_H - MARGIN_T - MARGIN_B - FOOTER_H,
                  leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
    cb = make_page_callbacks(q_num, q_title)
    tpl = PageTemplate(id="main", frames=[frame], onPage=cb)
    doc = BaseDocTemplate(path, pagesize=A4,
                          leftMargin=MARGIN_L, rightMargin=MARGIN_R,
                          topMargin=MARGIN_T, bottomMargin=MARGIN_B + FOOTER_H)
    doc.addPageTemplates([tpl])
    doc.build(story)
    print(f"  ✓  {filename}")
    return path

# ─── Helpers ──────────────────────────────────────────────────────────────────
def rule():
    return HRFlowable(width="100%", thickness=0.7,
                      color=C_RULE, spaceAfter=6, spaceBefore=4)

def sp(h=6):
    return Spacer(1, h)

def h1(text): return Paragraph(text, ST["h1"])
def h2(text): return Paragraph(text, ST["h2"])
def body(text): return Paragraph(text, ST["body"])
def bullet(text): return Paragraph(f"• {text}", ST["bullet"])
def caption(text): return Paragraph(text, ST["caption"])
def label(text): return Paragraph(text, ST["label"])
def center(text): return Paragraph(text, ST["center"])

def code_block(lines):
    """Return a shaded code block from a list of strings or a single string."""
    if isinstance(lines, str):
        lines = lines.split("\n")
    rows = [[Paragraph(ln, ST["code"])] for ln in lines]
    t = Table(rows, colWidths=[USABLE_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_CODE),
        ("BOX",        (0,0), (-1,-1), 0.5, C_BORDER),
        ("LEFTPADDING",(0,0), (-1,-1), 6),
        ("RIGHTPADDING",(0,0),(-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("ROWPADDING", (0,0), (-1,-1), 1),
    ]))
    return KeepTogether([t, sp(4)])

def img_box(filename, cap_text, max_h=None):
    path = os.path.join(SS_DIR, filename)
    if not os.path.exists(path):
        return body(f"[Screenshot not found: {filename}]")
    with PILImage.open(path) as im:
        orig_w, orig_h = im.size
    aspect = orig_h / orig_w
    w = USABLE_W
    h = w * aspect
    if max_h and h > max_h:
        h = max_h
        w = h / aspect
    img = RLImage(path, width=w, height=h)
    cap = caption(f"<b>Fig:</b> {cap_text}")
    return KeepTogether([img, cap, sp(4)])

def simple_table(headers, rows, col_widths=None):
    if col_widths is None:
        col_widths = [USABLE_W / len(headers)] * len(headers)
    data = [[Paragraph(f"<b>{h}</b>", ST["code"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), ST["body"]) for c in row])
    t = Table(data, colWidths=col_widths)
    ts = TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  C_TABLE_HEAD),
        ("TEXTCOLOR",    (0,0), (-1,0),  colors.white),
        ("FONTNAME",     (0,0), (-1,0),  BOLD_FONT),
        ("FONTSIZE",     (0,0), (-1,0),  9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, C_TABLE_ALT]),
        ("BOX",          (0,0), (-1,-1), 0.5, C_BORDER),
        ("INNERGRID",    (0,0), (-1,-1), 0.3, C_BORDER),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ])
    t.setStyle(ts)
    return KeepTogether([t, sp(6)])

# ══════════════════════════════════════════════════════════════════════════════
#  Q1 — Records of All Experiments
# ══════════════════════════════════════════════════════════════════════════════
def build_q1():
    story = []
    story += [
        h1("Question 1 — Records of All Experiments"),
        rule(),
        body(f"<b>Course:</b> {COURSE} &nbsp;&nbsp; <b>Lab:</b> {LAB}"),
        body(f"<b>Student:</b> {STUDENT} &nbsp;&nbsp; <b>Roll No.:</b> {ROLL} &nbsp;&nbsp; <b>Email:</b> {EMAIL}"),
        body(f"<b>Repository:</b> {REPO_URL}"),
        sp(8),
        body(
            "This record consolidates the evidence of all seven experiments performed in DevOps Lab 1. "
            "It includes the complete Git commit history, terminal screenshots, Jenkins console logs, "
            "deployment evidence and the Flask application response — all captured from the student's "
            "own environment on <b>Windows 11 / WSL2 Ubuntu 24.04 LTS</b>."
        ),
        sp(10),
    ]

    # Commit history
    story += [
        h2("1. Git Commit History"),
        body("The following commits were made to the main branch of the project repository:"),
        sp(4),
        code_block([
            "$ git log --oneline --graph --decorate",
            "* 2368328 (HEAD -> main, origin/main) record deployed app response",
            "* 518c993 add build logs, polling evidence and app screenshots",
            "* 7530c85 bump app version to 1.0.1 and add lab observations",
            "* 8946b3f record git push evidence",
            "* 600750c render terminal screenshots from command logs",
            "* a19ed32 add lab evidence: command logs and setup screenshots",
            "* f927337 add Jenkinsfile pipeline stages and deploy script",
            "* eecbcaa (tag: v1.0.0, feature/unit-tests) add pytest unit tests",
            "* 9d6906f initial commit: flask app with health endpoint",
        ]),
        sp(4),
    ]

    # Q4 evidence
    story += [
        h2("2. Q4 — Git Installation & Configuration"),
        img_box("q4-git-setup.png",        "Git version and global user configuration", max_h=200),
        img_box("q4-jenkins-install-1.png", "Java & Jenkins installation output — Part 1", max_h=200),
        img_box("q4-jenkins-install-2.png", "Jenkins service status — active (running)", max_h=200),
        img_box("04-jenkins-dashboard.png", "Jenkins web dashboard (first-time setup complete)", max_h=180),
        img_box("05-jenkins-plugins-installed.png","Suggested plugins installed", max_h=180),
    ]

    # Q5 evidence
    story += [
        h2("3. Q5 — Git Version Control"),
        img_box("q5-git-workflow-1.png", "git init, add, commit and branch creation", max_h=200),
        img_box("q5-git-workflow-2.png", "Branch merge, tag and log output", max_h=200),
        img_box("q5-local-test-run.png", "pytest execution — 2 tests passed", max_h=200),
        img_box("q5-push-github.png",    "git push to remote repository", max_h=200),
    ]

    # Q6/Q7 evidence
    story += [
        h2("4. Q6 & Q7 — Jenkins Pipeline (Build #1)"),
        img_box("06-pipeline-job.png",          "Jenkins pipeline job created", max_h=160),
        img_box("10-job-config-pipeline-scm.png","Pipeline SCM configuration", max_h=160),
        img_box("11-job-config-triggers.png",    "Poll SCM trigger configuration", max_h=160),
        img_box("07-build1-stage-graph.png",     "Build #1 stage view — all stages passed", max_h=160),
        img_box("08-build1-pipeline-overview.png","Build #1 pipeline overview", max_h=160),
        img_box("q6-q7-build1-console-1.png",   "Build #1 console — Checkout stage", max_h=200),
        img_box("q6-q7-build1-console-2.png",   "Build #1 console — Build stage", max_h=200),
        img_box("q6-q7-build1-console-3.png",   "Build #1 console — Test stage", max_h=200),
        img_box("q6-q7-build1-console-4.png",   "Build #1 console — Package stage", max_h=200),
        img_box("q6-q7-build1-console-5.png",   "Build #1 console — Deploy stage & SUCCESS", max_h=200),
    ]

    # Q3 evidence
    story += [
        h2("5. Q3 — Automated Deployment (Build #2)"),
        img_box("11-job-config-triggers.png",   "Poll SCM trigger active", max_h=160),
        img_box("q3-build2-console-1.png",      "Build #2 console — Checkout", max_h=200),
        img_box("q3-build2-console-2.png",      "Build #2 console — Build & Test", max_h=200),
        img_box("q3-build2-console-3.png",      "Build #2 console — Package & Deploy", max_h=200),
        img_box("q3-build2-console-4.png",      "Build #2 console — SUCCESS", max_h=200),
        img_box("13-git-polling-log.png",        "Git SCM polling log", max_h=160),
        img_box("14-build2-pipeline-overview.png","Build #2 pipeline overview", max_h=160),
        img_box("q3-deploy-verify.png",          "Deploy script execution on server", max_h=200),
        img_box("q3-auto-deploy-verify.png",     "Automated deployment verification", max_h=200),
        img_box("q3-deploy-after-pipeline.png",  "Service status after pipeline", max_h=200),
        img_box("q3-app-response.png",           "Flask app health endpoint — HTTP 200", max_h=180),
    ]

    story += [
        sp(10),
        h2("6. Conclusion"),
        body(
            "All seven experiments were successfully completed. The project demonstrates a full DevOps "
            "workflow: source code management with Git, continuous integration with Jenkins, automated "
            "testing with pytest, application packaging and automated deployment of a Flask application "
            "as a systemd service. The pipeline triggered automatically on every Git push via Poll SCM."
        ),
    ]
    build_doc("q1-records.pdf", "1", "Records of All Experiments", story)

# ══════════════════════════════════════════════════════════════════════════════
#  Q2 — CI/CD Workflow Report
# ══════════════════════════════════════════════════════════════════════════════
def build_q2():
    story = []
    story += [
        h1("Question 2 — CI/CD Workflow Report"),
        rule(),
        body(f"<b>Student:</b> {STUDENT} &nbsp;&nbsp; <b>Roll No.:</b> {ROLL}"),
        sp(6),
        body(
            "This report documents the complete Continuous Integration / Continuous Deployment (CI/CD) "
            "workflow implemented in DevOps Lab 1 using Git and Jenkins."
        ),
        sp(10),
    ]

    story += [
        h2("1. Aim"),
        body(
            "Design and implement a CI/CD pipeline that automatically builds, tests, packages and deploys "
            "a Python Flask web application whenever a commit is pushed to the Git repository."
        ),
        sp(6),
        h2("2. Tools & Technologies"),
        simple_table(
            ["Tool", "Version", "Purpose"],
            [
                ["Git",     "2.53.0", "Source code version control"],
                ["GitHub",  "—",      "Remote repository hosting"],
                ["Jenkins", "2.504.x","CI/CD automation server"],
                ["Python",  "3.12.10","Application runtime"],
                ["Flask",   "3.1.0",  "Web application framework"],
                ["pytest",  "8.x",    "Unit testing framework"],
                ["WSL2",    "Ubuntu 24.04", "Linux execution environment"],
            ],
            col_widths=[3*cm, 2.5*cm, USABLE_W-5.5*cm],
        ),
        sp(6),
    ]

    story += [
        h2("3. CI/CD Architecture"),
        body(
            "The pipeline follows a five-stage declarative Jenkinsfile model. Jenkins polls the GitHub "
            "repository every minute. On detecting a new commit it triggers the pipeline automatically."
        ),
        sp(4),
        code_block([
            "Developer pushes code",
            "        │",
            "        ▼",
            "Jenkins (Poll SCM — every minute)",
            "        │",
            "   ┌────┴─────────────────────────────────────┐",
            "   │  Stage 1: Checkout  → git checkout main  │",
            "   │  Stage 2: Build     → pip install         │",
            "   │  Stage 3: Test      → pytest -v           │",
            "   │  Stage 4: Package   → tar → artifact      │",
            "   │  Stage 5: Deploy    → deploy.sh           │",
            "   └────────────────────────────────────────────┘",
            "        │",
            "        ▼",
            "Flask app running on http://localhost:5000",
        ]),
        sp(6),
    ]

    story += [
        h2("4. Pipeline Stages"),
        simple_table(
            ["Stage", "Description", "Key Command"],
            [
                ["Checkout","Pull latest code from GitHub","checkout scm"],
                ["Build",   "Create virtualenv, install Flask","pip install -r app/requirements.txt"],
                ["Test",    "Run pytest unit tests","python -m pytest tests/ -v"],
                ["Package", "Archive build artefact","tar czf → archiveArtifacts"],
                ["Deploy",  "Copy files, restart service, health-check","bash scripts/deploy.sh"],
            ],
            col_widths=[2.5*cm, USABLE_W*0.42, USABLE_W*0.42],
        ),
        sp(6),
    ]

    story += [
        h2("5. Automation Results"),
        simple_table(
            ["Build #", "Trigger", "Commit", "Result", "Duration"],
            [
                ["#1", "Build Now (manual)", "f927337 — Jenkinsfile + deploy script", "SUCCESS ✓", "29 s"],
                ["#2", "Poll SCM (auto)",    "7530c85 — bump app version to 1.0.1",   "SUCCESS ✓", "17 s"],
            ],
            col_widths=[1.4*cm, 3.2*cm, USABLE_W-9*cm, 2.2*cm, 2.2*cm],
        ),
        sp(6),
    ]

    story += [
        h2("6. Evidence Screenshots"),
        img_box("08-build1-stage-graph.png",     "Build #1 stage view — all stages passed", max_h=170),
        img_box("13-git-polling-log.png",         "Git SCM polling log showing trigger", max_h=170),
        img_box("q3-auto-deploy-verify.png",      "Automated deployment verification", max_h=200),
        img_box("q5-local-test-run.png",          "pytest local test run — 2 passed", max_h=180),
        sp(6),
        h2("7. Observations"),
        bullet("The Poll SCM trigger detected commits within 60 seconds of a git push."),
        bullet("Both builds completed successfully with no test failures."),
        bullet("The Flask application was reachable at http://localhost:5000 after each deployment."),
        bullet("The /health endpoint returned HTTP 200 with JSON payload after every pipeline run."),
        sp(6),
        h2("8. Conclusion"),
        body(
            "The CI/CD pipeline successfully automated the full software delivery lifecycle — from "
            "source control through build, test, package and deployment — with zero manual intervention "
            "after the initial configuration."
        ),
    ]
    build_doc("q2-cicd-workflow-report.pdf", "2", "CI/CD Workflow Report", story)

# ══════════════════════════════════════════════════════════════════════════════
#  Q3 — Automate Application Deployment
# ══════════════════════════════════════════════════════════════════════════════
def build_q3():
    story = []
    story += [
        h1("Question 3 — Automate Application Deployment"),
        rule(),
        body(f"<b>Student:</b> {STUDENT} &nbsp;&nbsp; <b>Roll No.:</b> {ROLL}"),
        sp(6),
        h2("1. Aim"),
        body(
            "Automate the deployment of the Flask application so that every push to the Git repository "
            "triggers Jenkins to build, test and deploy the application without any manual step."
        ),
        sp(6),
        h2("2. Requirements"),
        bullet("Jenkins with the Git and Pipeline plugins installed."),
        bullet("A Poll SCM trigger configured to check the repository every minute."),
        bullet("deploy.sh script with sudo permission to copy files and restart the service."),
        bullet("A systemd service unit (devops-lab1.service) managing the Flask process."),
        sp(6),
    ]

    story += [
        h2("3. Poll SCM Configuration"),
        body(
            "The Jenkins job was configured with a <b>Poll SCM</b> trigger using the cron expression "
            "<b>* * * * *</b> (every minute). Jenkins polls the GitHub repository and triggers a new "
            "build only when it detects a new commit."
        ),
        sp(4),
        img_box("11-job-config-triggers.png", "Jenkins Poll SCM trigger — every minute", max_h=160),
        sp(4),
    ]

    story += [
        h2("4. Sudoers Configuration"),
        body(
            "The Jenkins user was granted passwordless sudo permission for the deploy script "
            "by adding the following line to <b>/etc/sudoers.d/jenkins</b>:"
        ),
        code_block(["jenkins ALL=(ALL) NOPASSWD: /bin/bash /var/lib/jenkins/workspace/devops-lab-1/scripts/deploy.sh"]),
        sp(4),
        h2("5. deploy.sh — Deployment Script"),
        code_block([
            "#!/bin/bash",
            "set -e",
            "",
            "APP_DIR=/opt/devops-lab1",
            "SERVICE_NAME=devops-lab1",
            "WORKSPACE=${WORKSPACE:-$(pwd)}",
            "",
            "echo '=== DevOps Lab 1 — Deployment Script ==='",
            "echo \"Workspace : $WORKSPACE\"",
            "echo \"Target    : $APP_DIR\"",
            "",
            "sudo mkdir -p $APP_DIR",
            "sudo cp -r $WORKSPACE/app $APP_DIR/",
            "sudo cp $WORKSPACE/app/requirements.txt $APP_DIR/",
            "",
            "cd $APP_DIR",
            "sudo python3 -m venv venv 2>/dev/null || true",
            "sudo $APP_DIR/venv/bin/pip install -q -r $APP_DIR/requirements.txt",
            "",
            "sudo cp $WORKSPACE/docs/devops-lab1.service /etc/systemd/system/devops-lab1.service",
            "sudo systemctl daemon-reload",
            "sudo systemctl enable devops-lab1",
            "sudo systemctl restart devops-lab1",
            "",
            "sleep 2",
            "STATUS=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:5000/health)",
            "if [ \"$STATUS\" = '200' ]; then",
            "    echo 'Health check PASSED — HTTP 200'",
            "else",
            "    echo \"Health check FAILED — HTTP $STATUS\" && exit 1",
            "fi",
        ]),
        sp(4),
    ]

    story += [
        h2("6. systemd Service Unit"),
        code_block([
            "[Unit]",
            "Description=DevOps Lab 1 Flask Application",
            "After=network.target",
            "",
            "[Service]",
            "User=www-data",
            "WorkingDirectory=/opt/devops-lab1",
            "ExecStart=/opt/devops-lab1/venv/bin/python -m flask --app app.app run --host=0.0.0.0",
            "Restart=always",
            "Environment=FLASK_ENV=production",
            "",
            "[Install]",
            "WantedBy=multi-user.target",
        ]),
        sp(6),
    ]

    story += [
        h2("7. Build #2 — Automated Trigger Evidence"),
        body(
            "After pushing commit <b>7530c85</b> (bump app version to 1.0.1), Jenkins automatically "
            "detected the change via Poll SCM and triggered Build #2."
        ),
        img_box("q3-build2-console-1.png", "Build #2 — Checkout stage console output", max_h=200),
        img_box("q3-build2-console-2.png", "Build #2 — Build & Test stage", max_h=200),
        img_box("q3-build2-console-3.png", "Build #2 — Package & Deploy stage", max_h=200),
        img_box("q3-build2-console-4.png", "Build #2 — Pipeline SUCCESS", max_h=200),
        img_box("13-git-polling-log.png",   "Git polling log showing automatic trigger", max_h=170),
        img_box("14-build2-pipeline-overview.png","Build #2 pipeline overview", max_h=160),
        img_box("q3-deploy-verify.png",     "deploy.sh execution on deployment server", max_h=200),
        img_box("q3-auto-deploy-verify.png","Service status verified — active (running)", max_h=200),
        img_box("q3-deploy-after-pipeline.png","App status after full pipeline", max_h=200),
        img_box("q3-app-response.png",      "Flask /health endpoint — HTTP 200 response", max_h=180),
        sp(6),
        h2("8. Observations"),
        bullet("Jenkins detected the commit within 60 seconds and started Build #2 automatically."),
        bullet("The deploy script copied application files, refreshed the virtualenv and restarted the service."),
        bullet("The health check inside deploy.sh confirmed HTTP 200 from the /health endpoint."),
        bullet("The systemd service remained active after deployment, confirming successful restart."),
        sp(6),
        h2("9. Conclusion"),
        body(
            "Full automated deployment was achieved. No manual intervention was required after the "
            "initial Jenkins job configuration. Every code commit triggered the pipeline, ensuring "
            "the latest version of the application was deployed and verified automatically."
        ),
    ]
    build_doc("q3-automate-deployment.pdf", "3", "Automate Application Deployment", story)

# ══════════════════════════════════════════════════════════════════════════════
#  Q4 — Install and Configure Git and Jenkins
# ══════════════════════════════════════════════════════════════════════════════
def build_q4():
    story = []
    story += [
        h1("Question 4 — Install and Configure Git and Jenkins"),
        rule(),
        body(f"<b>Student:</b> {STUDENT} &nbsp;&nbsp; <b>Roll No.:</b> {ROLL}"),
        sp(6),
        h2("1. Aim"),
        body(
            "Install Git and Jenkins on the development environment, perform the initial configuration "
            "of both tools, and verify that the Jenkins CI server is operational."
        ),
        sp(6),
        h2("2. Environment"),
        simple_table(
            ["Component", "Details"],
            [
                ["Host OS",   "Windows 11"],
                ["Linux env", "WSL2 — Ubuntu 24.04 LTS"],
                ["Git",       "2.53.0 (windows.2) on Windows / 2.43.0 on WSL Ubuntu"],
                ["Java",      "OpenJDK 17 (Temurin)"],
                ["Jenkins",   "2.504.x (LTS)"],
            ],
            col_widths=[4*cm, USABLE_W-4*cm],
        ),
        sp(6),
    ]

    story += [
        h2("3. Part A — Git Installation & Configuration"),
        body("Git was installed on Windows using the official installer from <b>git-scm.com</b>. "
             "In WSL2 Ubuntu it was installed via apt."),
        code_block([
            "# Windows (Git Bash / PowerShell)",
            "git --version",
            "# git version 2.53.0.windows.2",
            "",
            "# WSL2 Ubuntu",
            "sudo apt update && sudo apt install -y git",
            "git --version",
            "# git version 2.43.0",
            "",
            "# Global configuration (both environments)",
            'git config --global user.name  "Kartik"',
            'git config --global user.email "kartikjangra5366@gmail.com"',
            "git config --global init.defaultBranch main",
            "",
            "# Verify",
            "git config --global --list",
            "# user.name=Kartik",
            "# user.email=kartikjangra5366@gmail.com",
            "# init.defaultbranch=main",
        ]),
        img_box("q4-git-setup.png", "Git version and global user configuration", max_h=200),
        sp(4),
    ]

    story += [
        h2("4. Part B — Java & Jenkins Installation (WSL2 Ubuntu)"),
        body("Jenkins requires Java. OpenJDK 17 was installed first, then Jenkins LTS was added "
             "via its official apt repository."),
        code_block([
            "# Install Java 17",
            "sudo apt update",
            "sudo apt install -y fontconfig openjdk-17-jre",
            "java -version",
            "# openjdk version \"17.0.x\" ...",
            "",
            "# Add Jenkins repository key & source",
            "sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \\",
            "    https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key",
            "echo 'deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \\",
            "    https://pkg.jenkins.io/debian-stable binary/' \\",
            "    | sudo tee /etc/apt/sources.list.d/jenkins.list",
            "",
            "# Install Jenkins",
            "sudo apt update",
            "sudo apt install -y jenkins",
        ]),
        img_box("q4-jenkins-install-1.png", "Java & Jenkins apt installation output", max_h=200),
        sp(4),
    ]

    story += [
        h2("5. Part C — Jenkins Service & First-Time Setup"),
        code_block([
            "# Start and enable Jenkins service",
            "sudo systemctl start  jenkins",
            "sudo systemctl enable jenkins",
            "sudo systemctl status jenkins",
            "# ● jenkins.service - Jenkins Automation Server",
            "#      Loaded: loaded (/lib/systemd/system/jenkins.service; enabled)",
            "#      Active: active (running) since ...",
            "",
            "# Retrieve initial admin password",
            "sudo cat /var/lib/jenkins/secrets/initialAdminPassword",
        ]),
        img_box("q4-jenkins-install-2.png", "Jenkins systemctl status — active (running)", max_h=200),
        body("The Jenkins web interface was opened at <b>http://localhost:8080</b>. The initial "
             "admin password was entered, suggested plugins were installed and the first admin "
             "account was created."),
        img_box("04-jenkins-dashboard.png",          "Jenkins dashboard after first-time setup", max_h=170),
        img_box("05-jenkins-plugins-installed.png",  "Suggested plugins installation complete", max_h=170),
        sp(6),
        h2("6. Observations"),
        bullet("Git global configuration was identical on both Windows and WSL2 Ubuntu."),
        bullet("Jenkins service started successfully and was enabled to start on boot."),
        bullet("The suggested plugins included the Git plugin, Pipeline plugin and other essentials."),
        bullet("The Jenkins dashboard was accessible immediately after the first-time setup wizard."),
        sp(6),
        h2("7. Conclusion"),
        body(
            "Git and Jenkins were installed and configured successfully. The Jenkins CI server was "
            "operational, accessible via the web interface and ready to run pipeline jobs."
        ),
    ]
    build_doc("q4-install-configure-git-jenkins.pdf", "4",
              "Install and Configure Git and Jenkins", story)

# ══════════════════════════════════════════════════════════════════════════════
#  Q5 — Set Up Version Control Using Git
# ══════════════════════════════════════════════════════════════════════════════
def build_q5():
    story = []
    story += [
        h1("Question 5 — Set Up Version Control Using Git"),
        rule(),
        body(f"<b>Student:</b> {STUDENT} &nbsp;&nbsp; <b>Roll No.:</b> {ROLL}"),
        sp(6),
        h2("1. Aim"),
        body(
            "Initialise a Git repository for the Flask project, establish a branching strategy, "
            "create commits, merge branches, tag a release and push to a remote GitHub repository."
        ),
        sp(6),
        h2("2. Repository Details"),
        simple_table(
            ["Property", "Value"],
            [
                ["Repository name", "devops-lab-1"],
                ["Remote URL",      REPO_URL],
                ["Default branch",  "main"],
                ["Feature branch",  "feature/unit-tests"],
                ["Release tag",     "v1.0.0"],
                ["Author",          f"{STUDENT} <{EMAIL}>"],
            ],
            col_widths=[4*cm, USABLE_W-4*cm],
        ),
        sp(6),
    ]

    story += [
        h2("3. Step-by-Step Git Workflow"),
        label("Step 1 — Initialise & first commit"),
        code_block([
            "cd devops-lab-1-kartik",
            "git init",
            "git config user.name  'Kartik'",
            "git config user.email 'kartikjangra5366@gmail.com'",
            "",
            "git add README.md .gitignore app/",
            "git commit -m 'initial commit: flask app with health endpoint'",
        ]),
        label("Step 2 — Feature branch for unit tests"),
        code_block([
            "git checkout -b feature/unit-tests",
            "git add tests/test_app.py",
            "git commit -m 'add pytest unit tests for index and health routes'",
        ]),
        label("Step 3 — Merge & tag"),
        code_block([
            "git checkout main",
            "git merge feature/unit-tests",
            "git tag -a v1.0.0 -m 'first working version of the app'",
        ]),
        label("Step 4 — Add pipeline & deploy files"),
        code_block([
            "git add Jenkinsfile scripts/deploy.sh docs/devops-lab1.service",
            "git commit -m 'add Jenkinsfile pipeline stages and deploy script'",
        ]),
        label("Step 5 — Push to GitHub"),
        code_block([
            "git remote add origin " + REPO_URL,
            "git push -u origin main",
            "git push origin --tags",
        ]),
    ]

    story += [
        sp(4),
        h2("4. Evidence Screenshots"),
        img_box("q5-git-workflow-1.png", "git init, add, commit and feature branch creation", max_h=200),
        img_box("q5-git-workflow-2.png", "Branch merge, v1.0.0 tag and git log --oneline", max_h=200),
        img_box("q5-local-test-run.png", "pytest execution — 2 tests passed", max_h=190),
        img_box("q5-push-github.png",    "git push to remote repository", max_h=190),
        sp(4),
    ]

    story += [
        h2("5. Final Commit History"),
        code_block([
            "$ git log --oneline --graph --decorate",
            "* 2368328 (HEAD -> main, origin/main) record deployed app response",
            "* 518c993 add build logs, polling evidence and app screenshots",
            "* 7530c85 bump app version to 1.0.1 and add lab observations",
            "* 8946b3f record git push evidence",
            "* 600750c render terminal screenshots from command logs",
            "* a19ed32 add lab evidence: command logs and setup screenshots",
            "* f927337 add Jenkinsfile pipeline stages and deploy script",
            "* eecbcaa (tag: v1.0.0, feature/unit-tests) add pytest unit tests",
            "* 9d6906f initial commit: flask app with health endpoint",
        ]),
        sp(6),
        h2("6. Observations"),
        bullet("git init created a local repository with a 'main' default branch."),
        bullet("The feature/unit-tests branch was merged cleanly into main with a fast-forward merge."),
        bullet("pytest confirmed both the index and health routes returned HTTP 200."),
        bullet("git push uploaded all commits and the v1.0.0 tag to the remote repository."),
        sp(6),
        h2("7. Conclusion"),
        body(
            "Version control was established using Git with a disciplined branching and tagging workflow. "
            "All project files are tracked and the repository is synchronised with the remote on GitHub."
        ),
    ]
    build_doc("q5-version-control-git.pdf", "5", "Set Up Version Control Using Git", story)

# ══════════════════════════════════════════════════════════════════════════════
#  Q6 — Basic Jenkins CI/CD Pipeline
# ══════════════════════════════════════════════════════════════════════════════
def build_q6():
    story = []
    story += [
        h1("Question 6 — Basic Jenkins CI/CD Pipeline"),
        rule(),
        body(f"<b>Student:</b> {STUDENT} &nbsp;&nbsp; <b>Roll No.:</b> {ROLL}"),
        sp(6),
        h2("1. Aim"),
        body(
            "Create a Jenkins pipeline job that uses the Jenkinsfile in the repository to automatically "
            "checkout, build, test, package and deploy the Flask application."
        ),
        sp(6),
        h2("2. Job Configuration"),
        simple_table(
            ["Setting", "Value"],
            [
                ["Job type",       "Multibranch / Pipeline"],
                ["Definition",     "Pipeline script from SCM"],
                ["SCM",            "Git"],
                ["Repository URL", REPO_URL],
                ["Branch",         "*/main"],
                ["Script path",    "Jenkinsfile"],
                ["Build trigger",  "Poll SCM — * * * * * (every minute)"],
            ],
            col_widths=[4.5*cm, USABLE_W-4.5*cm],
        ),
        img_box("06-pipeline-job.png",          "Jenkins pipeline job created and configured", max_h=170),
        img_box("10-job-config-pipeline-scm.png","SCM configuration — Git repository and branch", max_h=170),
        img_box("11-job-config-triggers.png",    "Build trigger — Poll SCM every minute", max_h=160),
        sp(6),
    ]

    story += [
        h2("3. Build #1 — First Manual Execution"),
        body(
            "Build #1 was triggered manually using <b>Build Now</b> to verify the full pipeline. "
            "All five stages completed successfully."
        ),
        img_box("07-build1-stage-graph.png",         "Build #1 stage view — all stages passed", max_h=170),
        img_box("08-build1-pipeline-overview.png",   "Build #1 pipeline overview — SUCCESS", max_h=160),
        sp(4),
        h2("4. Console Output — Build #1"),
        img_box("q6-q7-build1-console-1.png", "Console — Checkout stage", max_h=200),
        img_box("q6-q7-build1-console-2.png", "Console — Build stage (virtualenv + pip install)", max_h=200),
        img_box("q6-q7-build1-console-3.png", "Console — Test stage (pytest)", max_h=200),
        img_box("q6-q7-build1-console-4.png", "Console — Package stage (tar artefact)", max_h=200),
        img_box("q6-q7-build1-console-5.png", "Console — Deploy stage & Finished: SUCCESS", max_h=200),
        sp(6),
    ]

    story += [
        h2("5. Observations"),
        bullet("All five pipeline stages — Checkout, Build, Test, Package, Deploy — passed on Build #1."),
        bullet("The pip install step installed Flask 3.1.0 into an isolated virtualenv."),
        bullet("pytest reported 2 tests passed with no warnings."),
        bullet("The deploy script confirmed HTTP 200 from the /health endpoint after deployment."),
        bullet("Total build duration was approximately 29 seconds."),
        sp(6),
        h2("6. Conclusion"),
        body(
            "A fully functional Jenkins CI/CD pipeline was created using a declarative Jenkinsfile. "
            "Build #1 validated the entire pipeline end-to-end, confirming that every stage executes "
            "correctly and the application is deployed and healthy after each run."
        ),
    ]
    build_doc("q6-basic-jenkins-pipeline.pdf", "6", "Basic Jenkins CI/CD Pipeline", story)

# ══════════════════════════════════════════════════════════════════════════════
#  Q7 — Jenkinsfile Pipeline Stages
# ══════════════════════════════════════════════════════════════════════════════
def build_q7():
    jenkinsfile_text = """\
pipeline {
    agent any

    environment {
        APP_DIR  = '/opt/devops-lab1'
        VENV_DIR = 'venv'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code checked out.'
            }
        }

        stage('Build') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    ./${VENV_DIR}/bin/pip install --upgrade pip -q
                    ./${VENV_DIR}/bin/pip install -r app/requirements.txt -q
                    echo "Build complete — Flask installed."
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    ./${VENV_DIR}/bin/python -m pytest tests/ -v \\
                        --tb=short --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Package') {
            steps {
                sh '''
                    mkdir -p dist
                    tar -czf dist/app-build-${BUILD_NUMBER}.tar.gz app/
                    echo "Package created: dist/app-build-${BUILD_NUMBER}.tar.gz"
                '''
                archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                sh 'sudo bash scripts/deploy.sh'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully — application deployed.'
        }
        failure {
            echo 'Pipeline FAILED — check the console output.'
        }
    }
}"""

    story = []
    story += [
        h1("Question 7 — Jenkinsfile Pipeline Stages"),
        rule(),
        body(f"<b>Student:</b> {STUDENT} &nbsp;&nbsp; <b>Roll No.:</b> {ROLL}"),
        sp(6),
        h2("1. Aim"),
        body(
            "Define a declarative Jenkinsfile with five clearly separated pipeline stages "
            "(Checkout → Build → Test → Package → Deploy) and demonstrate that each stage "
            "executes successfully."
        ),
        sp(6),
    ]

    story += [
        h2("2. Complete Jenkinsfile"),
        code_block(jenkinsfile_text.split("\n")),
        sp(6),
    ]

    story += [
        h2("3. Stage Descriptions"),
        simple_table(
            ["Stage", "What it does", "Key step"],
            [
                ["Checkout","Clones / updates the repository from GitHub","checkout scm"],
                ["Build",   "Creates a Python virtualenv and installs Flask","pip install -r app/requirements.txt"],
                ["Test",    "Runs pytest; publishes JUnit XML report","python -m pytest tests/ -v"],
                ["Package", "Creates a tar.gz archive and stores it as a Jenkins artefact","archiveArtifacts"],
                ["Deploy",  "Runs deploy.sh — copies files, restarts systemd service, health-checks",
                 "sudo bash scripts/deploy.sh"],
            ],
            col_widths=[2.5*cm, USABLE_W*0.43, USABLE_W*0.38],
        ),
        sp(6),
    ]

    story += [
        h2("4. Post Block"),
        body(
            "The <b>post</b> block at the end of the pipeline prints a success or failure message "
            "depending on the overall pipeline result. The <b>Test</b> stage's post block always "
            "publishes the JUnit XML file even when tests fail."
        ),
        sp(6),
        h2("5. Execution Evidence"),
        img_box("08-build1-stage-graph.png",       "Build #1 — all five stages passed", max_h=170),
        img_box("14-build2-pipeline-overview.png", "Build #2 — triggered by Poll SCM", max_h=160),
        img_box("q6-q7-build1-console-3.png",      "Console — pytest 2 tests passed", max_h=200),
        img_box("q6-q7-build1-console-4.png",      "Console — Package and artefact archived", max_h=200),
        sp(6),
        h2("6. Observations"),
        bullet("The declarative syntax made the pipeline readable and easy to maintain."),
        bullet("Each stage is isolated — a failure in Test stops Deploy from running."),
        bullet("The Package stage archived the tar.gz so it is downloadable from the Jenkins UI."),
        bullet("The post block ensured the JUnit report was published even on test failures."),
        sp(6),
        h2("7. Conclusion"),
        body(
            "The Jenkinsfile defined a complete, production-style CI/CD pipeline with five stages. "
            "The declarative syntax, post conditions and artefact archiving make the pipeline "
            "robust, traceable and ready for a real-world project."
        ),
    ]
    build_doc("q7-jenkinsfile-pipeline-stages.pdf", "7",
              "Jenkinsfile Pipeline Stages", story)

# ══════════════════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════════════════
def main():
    print(f"\nGenerating PDF reports for {STUDENT} ({ROLL})...")
    print(f"Screenshots : {SS_DIR}")
    print(f"Output dir  : {RPT_DIR}\n")

    build_q1()
    build_q2()
    build_q3()
    build_q4()
    build_q5()
    build_q6()
    build_q7()

    # Verify
    pdfs = [f for f in os.listdir(RPT_DIR) if f.endswith(".pdf")]
    print(f"\n{'='*50}")
    print(f"All {len(pdfs)} PDFs generated:")
    for p in sorted(pdfs):
        size = os.path.getsize(os.path.join(RPT_DIR, p))
        print(f"  {p:50s} {size/1024:7.1f} KB")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
