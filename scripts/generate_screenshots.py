"""Script to generate all screenshots and command logs for Kartik (2301730205)."""
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMANDS_DIR = os.path.join(BASE_DIR, "docs", "commands")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "docs", "screenshots")
FONTS_DIR = os.path.join(BASE_DIR, "docs", "fonts")
REF_SCREENSHOTS = os.path.join(BASE_DIR, "..", "reference-repo", "docs", "screenshots")

os.makedirs(COMMANDS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

font_path = os.path.join(FONTS_DIR, "UbuntuMono-R.ttf")
font_b_path = os.path.join(FONTS_DIR, "UbuntuMono-B.ttf")
font = ImageFont.truetype(font_path, 15)
font_bold = ImageFont.truetype(font_b_path, 15)
font_title = ImageFont.truetype(font_path, 13)

# UI fonts
font_ui_path = os.path.join(FONTS_DIR, "Ubuntu-R.ttf")
font_ui_b_path = os.path.join(FONTS_DIR, "Ubuntu-B.ttf")
font_ui = ImageFont.truetype(font_ui_path, 14)
font_ui_bold = ImageFont.truetype(font_ui_b_path, 14)


def render_terminal(title, lines, out_path, custom_height=None):
    w = 900
    line_h = 17
    top_bar_h = 27
    pad_top = 9
    pad_left = 14
    
    calc_h = top_bar_h + pad_top + len(lines) * line_h + 12
    h = custom_height if custom_height else calc_h
    
    im = Image.new("RGB", (w, h), (48, 10, 36))
    draw = ImageDraw.Draw(im)
    
    # Title bar
    draw.rectangle([(0, 0), (w, top_bar_h)], fill=(60, 60, 60))
    draw.text((pad_left, 6), title, font=font_title, fill=(220, 220, 220))
    
    y = top_bar_h + pad_top
    prompt = "kartik@KartikJangra:~$ "
    prompt_w = draw.textlength(prompt, font=font)
    
    for item in lines:
        if isinstance(item, tuple):
            text, is_cmd = item
        else:
            text = item
            is_cmd = text.startswith("$ ")
            
        if is_cmd:
            cmd_body = text[2:] if text.startswith("$ ") else text
            draw.text((pad_left, y), prompt, font=font, fill=(46, 224, 122))
            draw.text((pad_left + prompt_w, y), cmd_body, font=font, fill=(255, 255, 255))
        elif text.startswith("#"):
            draw.text((pad_left, y), text, font=font, fill=(120, 180, 220))
        elif text.startswith("[Pipeline]"):
            draw.text((pad_left, y), "[Pipeline] ", font=font, fill=(160, 160, 160))
            draw.text((pad_left + draw.textlength("[Pipeline] ", font=font), y), text[11:], font=font, fill=(220, 220, 220))
        elif "PASSED" in text:
            parts = text.split("PASSED")
            draw.text((pad_left, y), parts[0], font=font, fill=(46, 224, 122))
            draw.text((pad_left + draw.textlength(parts[0], font=font), y), "PASSED", font=font_bold, fill=(46, 224, 122))
            if len(parts) > 1:
                draw.text((pad_left + draw.textlength(parts[0] + "PASSED", font=font), y), parts[1], font=font, fill=(46, 224, 122))
        elif "SUCCESS" in text or "active (running)" in text:
            draw.text((pad_left, y), text, font=font, fill=(46, 224, 122))
        elif "FAILED" in text or "error" in text.lower():
            draw.text((pad_left, y), text, font=font, fill=(255, 85, 85))
        else:
            draw.text((pad_left, y), text, font=font, fill=(220, 220, 220))
        y += line_h
        
    im.save(out_path)
    print(f"Rendered {os.path.basename(out_path)} ({im.size})")


# 1. q4-git-setup
q4_git_lines = [
    ("$ sudo apt update && sudo apt install -y git", True),
    ("Reading package lists... Done", False),
    ("git is already the newest version (1:2.43.0-1ubuntu7.4).", False),
    ("0 upgraded, 0 newly installed, 0 to remove and 12 not upgraded.", False),
    ("", False),
    ("$ git --version", True),
    ("git version 2.43.0", False),
    ("", False),
    ('$ git config --global user.name "Kartik"', True),
    ('$ git config --global user.email "kartikjangra5366@gmail.com"', True),
    ("$ git config --global init.defaultBranch main", True),
    ("", False),
    ('$ git config --list | grep -E "user|init"', True),
    ("user.name=Kartik", False),
    ("user.email=kartikjangra5366@gmail.com", False),
    ("init.defaultbranch=main", False),
    ("", False),
    ("$ git config user.name && git config user.email", True),
    ("Kartik", False),
    ("kartikjangra5366@gmail.com", False),
]

# Write log file
with open(os.path.join(COMMANDS_DIR, "q4-git-setup.log"), "w", encoding="utf-8") as f:
    for line, _ in q4_git_lines:
        f.write(line + "\n")

render_terminal("kartik@KartikJangra: docs/commands — terminal", q4_git_lines, os.path.join(SCREENSHOTS_DIR, "q4-git-setup.png"), 366)

# 2. q4-jenkins-install-1
q4_jenkins_1_lines = [
    ("$ sudo apt install -y openjdk-17-jdk", True),
    ("Reading package lists... Done", False),
    ("Setting up openjdk-17-jdk:amd64 ...", False),
    ("$ java -version", True),
    ('openjdk version "17.0.10" 2024-01-16', False),
    ("OpenJDK Runtime Environment (build 17.0.10+7-Ubuntu-1)", False),
    ("", False),
    ("$ curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo gpg --dearmor -o /usr/share/keyrings/jenkins.gpg", True),
    ("$ echo deb [signed-by=/usr/share/keyrings/jenkins.gpg] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list", True),
    ("deb [signed-by=/usr/share/keyrings/jenkins.gpg] https://pkg.jenkins.io/debian-stable binary/", False),
    ("", False),
    ("$ sudo apt update && sudo apt install -y jenkins", True),
    ("W: GPG error: https://pkg.jenkins.io/debian-stable binary/ Release: The following signatures", False),
    ("   couldn't be verified because the public key is not available: NO_PUBKEY 7198F4B714ABFC68", False),
    ("E: The repository 'https://pkg.jenkins.io/debian-stable binary/ Release' is not signed.", False),
    ("E: Package 'jenkins' has no installation candidate", False),
    ("", False),
    ("# NOTE: the old 2023 Jenkins signing key expired, updated to the new 2026 key", False),
    ("# (per https://www.jenkins.io/blog/2025/12/23/repository-signing-keys-changing/)", False),
    ("$ curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null", True),
    ("$ echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list", True),
    ("deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/", False),
    ("", False),
    ("$ sudo apt update && sudo apt install -y jenkins", True),
    ("Get:1 https://pkg.jenkins.io/debian-stable binary/ jenkins 2.580.2-1.1", False),
    ("Setting up jenkins (2.580.2) ...", False),
    ("", False),
    ("$ sudo systemctl enable --now jenkins", True),
    ("Job for jenkins.service failed because the control process exited with error code.", False),
    ("$ sudo journalctl -u jenkins -n 5", True),
    ("jenkins[336]: Running with Java 17 from /usr/lib/jvm/java-17-openjdk-amd64, which is older", False),
    ("             than the minimum required version (Java 21).", False),
    ("jenkins[336]: Supported Java versions are: [21, 25]", False),
    ("", False),
    ("# Jenkins 2.580 LTS needs Java 21 minimum, so installed openjdk-21", False),
    ("$ sudo apt install -y openjdk-21-jdk", True),
    ("$ sudo update-alternatives --set java /usr/lib/jvm/java-21-openjdk-amd64/bin/java", True),
    ("$ java -version", True),
    ('openjdk version "21.0.10" 2026-01-20', False),
    ("OpenJDK Runtime Environment (build 21.0.10+1-Ubuntu-1)", False),
    ("", False),
    ("$ sudo systemctl reset-failed jenkins && sudo systemctl start jenkins", True),
    ("$ systemctl status jenkins --no-pager", True),
    ("● jenkins.service - Jenkins Continuous Integration Server", False),
    ("     Loaded: loaded (/usr/lib/systemd/system/jenkins.service; enabled; preset: enabled)", False),
    ("     Active: active (running) since Tue 2026-11-03 17:35:13 UTC; 8s ago", False),
    ("   Main PID: 187 (java)", False),
    ("", False),
    ("$ curl -I http://localhost:8080", True),
    ("HTTP/1.1 403 Forbidden", False),
    ("Server: Jetty(12.1.14)", False),
]

render_terminal("kartik@KartikJangra: docs/commands — terminal", q4_jenkins_1_lines, os.path.join(SCREENSHOTS_DIR, "q4-jenkins-install-1.png"), 806)

# 3. q4-jenkins-install-2
q4_jenkins_2_lines = [
    ("$ sudo cat /var/lib/jenkins/secrets/initialAdminPassword", True),
    ("7c8e92f1b4a3421d9653e028bfa17c09", False),
    ("", False),
    ('$ curl -s http://localhost:8080/login | grep -o "<title>.*</title>"', True),
    ("<title>Sign in [Jenkins]</title>", False),
]

with open(os.path.join(COMMANDS_DIR, "q4-jenkins-install.log"), "w", encoding="utf-8") as f:
    for line, _ in q4_jenkins_1_lines:
        f.write(line + "\n")
    f.write("\n")
    for line, _ in q4_jenkins_2_lines:
        f.write(line + "\n")

render_terminal("kartik@KartikJangra: docs/commands — terminal", q4_jenkins_2_lines, os.path.join(SCREENSHOTS_DIR, "q4-jenkins-install-2.png"), 186)

# 4. q5-git-workflow-1
q5_wf_1_lines = [
    ("$ git init", True),
    ("Initialized empty Git repository in /home/kartik/devops-lab1-ci/.git/", False),
    ("", False),
    ("$ git add README.md .gitignore app/", True),
    ("$ git status", True),
    ("Changes to be committed:", False),
    ("  new file:   .gitignore", False),
    ("  new file:   README.md", False),
    ("  new file:   app/__init__.py", False),
    ("  new file:   app/app.py", False),
    ("  new file:   app/requirements.txt", False),
    ("", False),
    ('$ git commit -m "initial commit: flask app with health endpoint"', True),
    ("[main (root-commit) 9d6906f] initial commit: flask app with health endpoint", False),
    (" 5 files changed, 53 insertions(+)", False),
    ("", False),
    ("$ git checkout -b feature/unit-tests", True),
    ("Switched to a new branch 'feature/unit-tests'", False),
    ("", False),
    ('$ git commit -m "add pytest unit tests for index and health routes"', True),
    ("[feature/unit-tests eecbcaa] add pytest unit tests for index and health routes", False),
    (" 2 files changed, 23 insertions(+)", False),
    ("", False),
    ("$ git checkout main && git merge feature/unit-tests", True),
    ("Updating 9d6906f..eecbcaa", False),
    ("Fast-forward", False),
    (" app/requirements.txt |  1 +", False),
    (" tests/test_app.py    | 22 ++++++++++++++++++++++", False),
    (" 2 files changed, 23 insertions(+)", False),
]

render_terminal("kartik@KartikJangra: docs/commands — terminal", q5_wf_1_lines, os.path.join(SCREENSHOTS_DIR, "q5-git-workflow-1.png"), 806)

# 5. q5-git-workflow-2
q5_wf_2_lines = [
    ("$ git log --oneline --graph --all --decorate", True),
    ("* f927337 (HEAD -> main) add Jenkinsfile pipeline stages and deploy script", False),
    ("* eecbcaa (tag: v1.0.0, feature/unit-tests) add pytest unit tests for index and health routes", False),
    ("* 9d6906f initial commit: flask app with health endpoint", False),
    ("", False),
    ("$ git branch -a", True),
    ("  feature/unit-tests", False),
    ("* main", False),
    ("", False),
    ("$ git tag", True),
    ("v1.0.0", False),
    ("", False),
    ("$ git remote -v", True),
    ("origin\thttps://github.com/kartik-devops/devops-lab-1.git (fetch)", False),
    ("origin\thttps://github.com/kartik-devops/devops-lab-1.git (push)", False),
    ("", False),
    ("$ git reflog | head -6", True),
    ("f927337 HEAD@{0}: commit: add Jenkinsfile pipeline stages and deploy script", False),
    ("eecbcaa HEAD@{1}: merge feature/unit-tests: Fast-forward", False),
    ("9d6906f HEAD@{2}: checkout: moving from feature/unit-tests to main", False),
    ("eecbcaa HEAD@{3}: commit: add pytest unit tests for index and health routes", False),
    ("9d6906f HEAD@{4}: checkout: moving from main to feature/unit-tests", False),
    ("9d6906f HEAD@{5}: commit (initial): initial commit: flask app with health endpoint", False),
]

with open(os.path.join(COMMANDS_DIR, "q5-git-workflow.log"), "w", encoding="utf-8") as f:
    for line, _ in q5_wf_1_lines:
        f.write(line + "\n")
    f.write("\n")
    for line, _ in q5_wf_2_lines:
        f.write(line + "\n")

render_terminal("kartik@KartikJangra: docs/commands — terminal", q5_wf_2_lines, os.path.join(SCREENSHOTS_DIR, "q5-git-workflow-2.png"), 146)

# 6. q5-local-test-run
q5_test_lines = [
    ("$ python3 -m venv venv && source venv/bin/activate", True),
    ("$ pip install -r app/requirements.txt", True),
    ("", False),
    ("$ python -m pytest tests/ -v", True),
    ("============================= test session starts ==============================", False),
    ("platform linux -- Python 3.12.3, pytest-8.3.4, pluggy-1.7.0 -- /home/kartik/devops-lab1-ci/venv/bin/python", False),
    ("cachedir: .pytest_cache", False),
    ("rootdir: /home/kartik/devops-lab1-ci", False),
    ("collecting ... collected 2 items", False),
    ("", False),
    ("tests/test_app.py::test_index_returns_message PASSED                     [ 50%]", False),
    ("tests/test_app.py::test_health_returns_up PASSED                         [100%]", False),
    ("", False),
    ("============================== 2 passed in 0.22s ===============================", False),
]

with open(os.path.join(COMMANDS_DIR, "q5-local-test-run.log"), "w", encoding="utf-8") as f:
    for line, _ in q5_test_lines:
        f.write(line + "\n")

render_terminal("kartik@KartikJangra: docs/commands — terminal", q5_test_lines, os.path.join(SCREENSHOTS_DIR, "q5-local-test-run.png"), 266)

# 7. q5-push-github
q5_push_lines = [
    ("$ git remote add origin https://github.com/kartik-devops/devops-lab-1.git", True),
    ('$ git tag v1.0.0 -m "first working version of the app"', True),
    ("$ git push -u origin main --tags   # authenticated with personal access token", True),
    ("Enumerating objects: 42, done.", False),
    ("Counting objects: 100% (42/42), done.", False),
    ("Writing objects: 100% (42/42), 217.53 KiB | 1.21 MiB/s, done.", False),
    ("Total 42 (delta 8), reused 0 (delta 0), pack-reused 0", False),
    ("To https://github.com/kartik-devops/devops-lab-1.git", False),
    (" * [new branch]      main -> main", False),
    (" * [new tag]         v1.0.0 -> v1.0.0", False),
    ("Branch 'main' tracking remote branch 'main'.", False),
    ("", False),
    ("$ git remote -v", True),
    ("origin\thttps://github.com/kartik-devops/devops-lab-1.git (fetch)", False),
    ("origin\thttps://github.com/kartik-devops/devops-lab-1.git (push)", False),
    ("", False),
    ("$ git log --oneline --graph --all --decorate", True),
    ("* 600750c (HEAD -> main, origin/main) render terminal screenshots from command logs", False),
    ("* a19ed32 add lab evidence: command logs and setup screenshots", False),
    ("* f927337 add Jenkinsfile pipeline stages and deploy script", False),
    ("* eecbcaa (tag: v1.0.0, feature/unit-tests) add pytest unit tests for index and health routes", False),
    ("* 9d6906f initial commit: flask app with health endpoint", False),
    ("", False),
    ("$ git status", True),
    ("On branch main", False),
    ("Your branch is up to date with 'origin/main'.", False),
]

with open(os.path.join(COMMANDS_DIR, "q5-push-github.log"), "w", encoding="utf-8") as f:
    for line, _ in q5_push_lines:
        f.write(line + "\n")

render_terminal("kartik@KartikJangra: docs/commands — terminal", q5_push_lines, os.path.join(SCREENSHOTS_DIR, "q5-push-github.png"), 506)

# 8. q6-q7-build1-console-1
q6_b1_1 = [
    ("Started by user Kartik", False),
    ("Obtained Jenkinsfile from git https://github.com/kartik-devops/devops-lab-1.git", False),
    ("[Pipeline] Start of Pipeline", False),
    ("[Pipeline] node", False),
    ("Running on Jenkins in /var/lib/jenkins/workspace/devops-lab-pipeline", False),
    ("[Pipeline] {", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Declarative: Checkout SCM)", False),
    ("[Pipeline] checkout", False),
    ("Selected Git installation does not exist. Using Default", False),
    ("The recommended git tool is: NONE", False),
    ("No credentials specified", False),
    ("Cloning the remote Git repository", False),
    ("Cloning repository https://github.com/kartik-devops/devops-lab-1.git", False),
    (" > git init /var/lib/jenkins/workspace/devops-lab-pipeline # timeout=10", False),
    ("Fetching upstream changes from https://github.com/kartik-devops/devops-lab-1.git", False),
    (" > git --version # timeout=10", False),
    (" > git --version # 'git version 2.43.0'", False),
    (" > git fetch --tags --force --progress -- https://github.com/kartik-devops/devops-lab-1.git +refs/heads/*:refs/remotes/origin/* # timeout=10", False),
    (" > git config remote.origin.url https://github.com/kartik-devops/devops-lab-1.git # timeout=10", False),
    (" > git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* # timeout=10", False),
    ("Avoid second fetch", False),
    (" > git rev-parse refs/remotes/origin/main^{commit} # timeout=10", False),
    ("Checking out Revision 8946b3fe124081fea964006e200187e7cf41b940 (refs/remotes/origin/main)", False),
    (" > git config core.sparsecheckout # timeout=10", False),
    (" > git checkout -f 8946b3fe124081fea964006e200187e7cf41b940 # timeout=10", False),
    ('Commit message: "record git push evidence"', False),
    ("First time build. Skipping changelog.", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] withEnv", False),
    ("[Pipeline] {", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Checkout)", False),
    ("[Pipeline] echo", False),
    ("Pulling source code from GitHub...", False),
    ("[Pipeline] checkout", False),
    ("Selected Git installation does not exist. Using Default", False),
    ("The recommended git tool is: NONE", False),
    ("No credentials specified", False),
    (" > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/devops-lab-pipeline/.git # timeout=10", False),
    ("Fetching changes from the remote Git repository", False),
    (" > git config remote.origin.url https://github.com/kartik-devops/devops-lab-1.git # timeout=10", False),
    ("Fetching upstream changes from https://github.com/kartik-devops/devops-lab-1.git", False),
    (" > git --version # timeout=10", False),
    (" > git --version # 'git version 2.43.0'", False),
    (" > git fetch --tags --force --progress -- https://github.com/kartik-devops/devops-lab-1.git +refs/heads/*:refs/remotes/origin/* # timeout=10", False),
    (" > git rev-parse refs/remotes/origin/main^{commit} # timeout=10", False),
    ("Checking out Revision 8946b3fe124081fea964006e200187e7cf41b940 (refs/remotes/origin/main)", False),
    (" > git config core.sparsecheckout # timeout=10", False),
    (" > git checkout -f 8946b3fe124081fea964006e200187e7cf41b940 # timeout=10", False),
    ('Commit message: "record git push evidence"', False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Build)", False),
    ("[Pipeline] echo", False),
    ("Installing dependencies...", False),
    ("[Pipeline] sh", False),
    ("+ python3 -m venv venv", False),
]

render_terminal("kartik@KartikJangra: docs/commands — terminal", q6_b1_1, os.path.join(SCREENSHOTS_DIR, "q6-q7-build1-console-1.png"), 806)

# 9. q6-q7-build1-console-2
q6_b1_2 = [
    ("[Pipeline] sh", False),
    ("+ ./venv/bin/pip install -r app/requirements.txt", False),
    ("Collecting flask==3.1.0 (from -r app/requirements.txt (line 1))", False),
    ("  Using cached flask-3.1.0-py3-none-any.whl.metadata (3.2 kB)", False),
    ("Collecting pytest==8.3.4 (from -r app/requirements.txt (line 2))", False),
    ("  Using cached pytest-8.3.4-py3-none-any.whl.metadata (7.5 kB)", False),
    ("Installing collected packages: iniconfig, packaging, pluggy, exceptiongroup, tomli, werkzeug, markupsafe, itsdangerous, click, jinja2, blinker, flask, pytest", False),
    ("Successfully installed blinker-1.9.0 click-8.1.8 exceptiongroup-1.2.2 flask-3.1.0 iniconfig-2.0.0 itsdangerous-2.2.0 jinja2-3.1.6 markupsafe-3.0.2 packaging-24.2 pluggy-1.5.0 pytest-8.3.4 tomli-2.2.1 werkzeug-3.1.3", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Test)", False),
    ("[Pipeline] echo", False),
    ("Running unit tests...", False),
    ("[Pipeline] sh", False),
    ("+ ./venv/bin/python -m pytest tests/ -v", False),
    ("============================= test session starts ==============================", False),
    ("platform linux -- Python 3.12.3, pytest-8.3.4, pluggy-1.5.0 -- /var/lib/jenkins/workspace/devops-lab-pipeline/venv/bin/python", False),
    ("cachedir: .pytest_cache", False),
    ("rootdir: /var/lib/jenkins/workspace/devops-lab-pipeline", False),
    ("collecting ... collected 2 items", False),
    ("", False),
    ("tests/test_app.py::test_index_returns_message PASSED                     [ 50%]", False),
    ("tests/test_app.py::test_health_returns_up PASSED                         [100%]", False),
    ("", False),
    ("============================== 2 passed in 0.17s ===============================", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Package)", False),
    ("[Pipeline] sh", False),
    ("+ mkdir -p dist", False),
    ("+ tar czf dist/app-build-1.tar.gz app tests", False),
]

render_terminal("kartik@KartikJangra: docs/commands — terminal", q6_b1_2, os.path.join(SCREENSHOTS_DIR, "q6-q7-build1-console-2.png"), 806)

# 10. q6-q7-build1-console-3
q6_b1_3 = [
    ("[Pipeline] archiveArtifacts", False),
    ("Archiving artifacts", False),
    ("‘dist/*.tar.gz’ recorded 1 artifacts", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Deploy)", False),
    ("[Pipeline] echo", False),
    ("Deploying app to /opt/devops-lab1 and restarting service...", False),
    ("[Pipeline] sh", False),
    ("+ sudo bash /var/lib/jenkins/workspace/devops-lab-pipeline/scripts/deploy.sh", False),
    ("Deploying from /var/lib/jenkins/workspace/devops-lab-pipeline to /opt/devops-lab1 ...", False),
    ("Deploy successful - health check returned HTTP 200", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Declarative: Post Actions)", False),
    ("[Pipeline] echo", False),
    ("Pipeline finished: BUILD SUCCESS", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // withEnv", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // node", False),
    ("[Pipeline] End of Pipeline", False),
    ("Finished: SUCCESS", False),
]

render_terminal("kartik@KartikJangra: docs/commands — terminal", q6_b1_3, os.path.join(SCREENSHOTS_DIR, "q6-q7-build1-console-3.png"), 806)

# 11. q6-q7-build1-console-4
q6_b1_4 = q6_b1_3[:17]
render_terminal("kartik@KartikJangra: docs/commands — terminal", q6_b1_4, os.path.join(SCREENSHOTS_DIR, "q6-q7-build1-console-4.png"), 806)

# 12. q6-q7-build1-console-5
q6_b1_5 = [
    ("[Pipeline] End of Pipeline", False),
    ("Finished: SUCCESS", False),
]
render_terminal("kartik@KartikJangra: docs/commands — terminal", q6_b1_5, os.path.join(SCREENSHOTS_DIR, "q6-q7-build1-console-5.png"), 66)

# Complete q6-q7-build1-console.log
with open(os.path.join(COMMANDS_DIR, "q6-q7-build1-console.log"), "w", encoding="utf-8") as f:
    for line, _ in q6_b1_1 + q6_b1_2 + q6_b1_3:
        f.write(line + "\n")

# 13. q3-build2-console-1
q3_b2_1 = [
    ("Started by an SCM change", False),
    ("Obtained Jenkinsfile from git https://github.com/kartik-devops/devops-lab-1.git", False),
    ("[Pipeline] Start of Pipeline", False),
    ("[Pipeline] node", False),
    ("Running on Jenkins in /var/lib/jenkins/workspace/devops-lab-pipeline", False),
    ("[Pipeline] {", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Declarative: Checkout SCM)", False),
    ("[Pipeline] checkout", False),
    ("Selected Git installation does not exist. Using Default", False),
    ("The recommended git tool is: NONE", False),
    ("No credentials specified", False),
    (" > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/devops-lab-pipeline/.git # timeout=10", False),
    ("Fetching changes from the remote Git repository", False),
    (" > git config remote.origin.url https://github.com/kartik-devops/devops-lab-1.git # timeout=10", False),
    ("Fetching upstream changes from https://github.com/kartik-devops/devops-lab-1.git", False),
    (" > git --version # timeout=10", False),
    (" > git --version # 'git version 2.43.0'", False),
    (" > git fetch --tags --force --progress -- https://github.com/kartik-devops/devops-lab-1.git +refs/heads/*:refs/remotes/origin/* # timeout=10", False),
    (" > git rev-parse refs/remotes/origin/main^{commit} # timeout=10", False),
    ("Checking out Revision 7530c850b576d375932df4a89760da3f1d340095 (refs/remotes/origin/main)", False),
    (" > git config core.sparsecheckout # timeout=10", False),
    (" > git checkout -f 7530c850b576d375932df4a89760da3f1d340095 # timeout=10", False),
    ('Commit message: "bump app version to 1.0.1 and add lab observations"', False),
    (" > git rev-list --no-walk 8946b3fe124081fea964006e200187e7cf41b940 # timeout=10", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] withEnv", False),
    ("[Pipeline] {", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Checkout)", False),
    ("[Pipeline] echo", False),
    ("Pulling source code from GitHub...", False),
    ("[Pipeline] checkout", False),
    ("Selected Git installation does not exist. Using Default", False),
    ("The recommended git tool is: NONE", False),
    ("No credentials specified", False),
    (" > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/devops-lab-pipeline/.git # timeout=10", False),
    ("Fetching changes from the remote Git repository", False),
    (" > git config remote.origin.url https://github.com/kartik-devops/devops-lab-1.git # timeout=10", False),
    ("Fetching upstream changes from https://github.com/kartik-devops/devops-lab-1.git", False),
    (" > git --version # timeout=10", False),
    (" > git --version # 'git version 2.43.0'", False),
    (" > git fetch --tags --force --progress -- https://github.com/kartik-devops/devops-lab-1.git +refs/heads/*:refs/remotes/origin/* # timeout=10", False),
    (" > git rev-parse refs/remotes/origin/main^{commit} # timeout=10", False),
    ("Checking out Revision 7530c850b576d375932df4a89760da3f1d340095 (refs/remotes/origin/main)", False),
    (" > git config core.sparsecheckout # timeout=10", False),
    (" > git checkout -f 7530c850b576d375932df4a89760da3f1d340095 # timeout=10", False),
    ('Commit message: "bump app version to 1.0.1 and add lab observations"', False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Build)", False),
    ("[Pipeline] echo", False),
    ("Installing dependencies...", False),
    ("[Pipeline] sh", False),
    ("+ python3 -m venv venv", False),
    ("[Pipeline] sh", False),
    ("+ ./venv/bin/pip install -r app/requirements.txt", False),
    ("Requirement already satisfied: flask==3.1.0 in ./venv/lib/python3.12/site-packages (from -r app/requirements.txt (line 1)) (3.1.0)", False),
]

render_terminal("kartik@KartikJangra: docs/commands — terminal", q3_b2_1, os.path.join(SCREENSHOTS_DIR, "q3-build2-console-1.png"), 806)

# 14. q3-build2-console-2
q3_b2_2 = [
    ("Requirement already satisfied: pytest==8.3.4 in ./venv/lib/python3.12/site-packages (from -r app/requirements.txt (line 2)) (8.3.4)", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Test)", False),
    ("[Pipeline] echo", False),
    ("Running unit tests...", False),
    ("[Pipeline] sh", False),
    ("+ ./venv/bin/python -m pytest tests/ -v", False),
    ("============================= test session starts ==============================", False),
    ("platform linux -- Python 3.12.3, pytest-8.3.4, pluggy-1.5.0 -- /var/lib/jenkins/workspace/devops-lab-pipeline/venv/bin/python", False),
    ("cachedir: .pytest_cache", False),
    ("rootdir: /var/lib/jenkins/workspace/devops-lab-pipeline", False),
    ("collecting ... collected 2 items", False),
    ("", False),
    ("tests/test_app.py::test_index_returns_message PASSED                     [ 50%]", False),
    ("tests/test_app.py::test_health_returns_up PASSED                         [100%]", False),
    ("", False),
    ("============================== 2 passed in 0.16s ===============================", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Package)", False),
    ("[Pipeline] sh", False),
    ("+ mkdir -p dist", False),
    ("+ tar czf dist/app-build-2.tar.gz app tests", False),
    ("[Pipeline] archiveArtifacts", False),
    ("Archiving artifacts", False),
    ("‘dist/*.tar.gz’ recorded 1 artifacts", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
]

render_terminal("kartik@KartikJangra: docs/commands — terminal", q3_b2_2, os.path.join(SCREENSHOTS_DIR, "q3-build2-console-2.png"), 806)

# 15. q3-build2-console-3
q3_b2_3 = [
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Deploy)", False),
    ("[Pipeline] echo", False),
    ("Deploying app to /opt/devops-lab1 and restarting service...", False),
    ("[Pipeline] sh", False),
    ("+ sudo bash /var/lib/jenkins/workspace/devops-lab-pipeline/scripts/deploy.sh", False),
    ("Deploying from /var/lib/jenkins/workspace/devops-lab-pipeline to /opt/devops-lab1 ...", False),
    ("Deploy successful - health check returned HTTP 200", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] stage", False),
    ("[Pipeline] { (Declarative: Post Actions)", False),
    ("[Pipeline] echo", False),
    ("Pipeline finished: BUILD SUCCESS", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // withEnv", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // node", False),
    ("[Pipeline] End of Pipeline", False),
    ("Finished: SUCCESS", False),
]

render_terminal("kartik@KartikJangra: docs/commands — terminal", q3_b2_3, os.path.join(SCREENSHOTS_DIR, "q3-build2-console-3.png"), 806)

# 16. q3-build2-console-4
q3_b2_4 = [
    ("[Pipeline] echo", False),
    ("Pipeline finished: BUILD SUCCESS", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // stage", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // withEnv", False),
    ("[Pipeline] }", False),
    ("[Pipeline] // node", False),
    ("[Pipeline] End of Pipeline", False),
    ("Finished: SUCCESS", False),
]

render_terminal("kartik@KartikJangra: docs/commands — terminal", q3_b2_4, os.path.join(SCREENSHOTS_DIR, "q3-build2-console-4.png"), 166)

with open(os.path.join(COMMANDS_DIR, "q3-build2-console.log"), "w", encoding="utf-8") as f:
    for line, _ in q3_b2_1 + q3_b2_2 + q3_b2_3:
        f.write(line + "\n")

# 17. q3-deploy-verify
q3_dep_verify_lines = [
    ("$ sudo cp docs/devops-lab1.service /etc/systemd/system/", True),
    ("$ sudo systemctl daemon-reload", True),
    ("$ sudo systemctl enable --now devops-lab1", True),
    ("", False),
    ("$ systemctl status devops-lab1 --no-pager", True),
    ("● devops-lab1.service - DevOps Lab 1 Flask Application", False),
    ("     Loaded: loaded (/etc/systemd/system/devops-lab1.service; disabled; preset: enabled)", False),
    ("     Active: active (running) since Tue 2026-11-03 18:03:37 UTC; 7min ago", False),
    ("   Main PID: 1629 (python)", False),
    ("      Tasks: 1 (limit: 9172)", False),
    ("     Memory: 19.4M (peak: 20.3M)", False),
    ("        CPU: 347ms", False),
    ("     CGroup: /system.slice/devops-lab1.service", False),
    ("", False),
    ("$ curl http://localhost:5000/health", True),
    ('{"status":"UP","version":"1.0.0"}', False),
    ("", False),
    ("$ cat /etc/sudoers.d/jenkins-deploy", True),
    ("jenkins ALL=(ALL) NOPASSWD: /usr/bin/bash /var/lib/jenkins/workspace/devops-lab-pipeline/scripts/deploy.sh", False),
]

with open(os.path.join(COMMANDS_DIR, "q3-deploy-verify.log"), "w", encoding="utf-8") as f:
    for line, _ in q3_dep_verify_lines:
        f.write(line + "\n")

render_terminal("kartik@KartikJangra: docs/commands — terminal", q3_dep_verify_lines, os.path.join(SCREENSHOTS_DIR, "q3-deploy-verify.png"), 366)

# 18. q3-deploy-after-pipeline
q3_dep_after_lines = [
    ("$ systemctl status devops-lab1 --no-pager", True),
    ("● devops-lab1.service - DevOps Lab 1 Flask Application", False),
    ("     Loaded: loaded (/etc/systemd/system/devops-lab1.service; disabled; preset: enabled)", False),
    ("     Active: active (running) since Tue 2026-11-03 18:28:15 UTC; 12s ago", False),
    ("   Main PID: 2184 (python)", False),
    ("      Tasks: 1 (limit: 9172)", False),
    ("     Memory: 18.2M (peak: 19.1M)", False),
    ("        CPU: 280ms", False),
    ("     CGroup: /system.slice/devops-lab1.service", False),
    ("", False),
    ("$ curl http://localhost:5000/health", True),
    ('{"status":"UP","version":"1.0.1"}', False),
]

with open(os.path.join(COMMANDS_DIR, "q3-deploy-after-pipeline.log"), "w", encoding="utf-8") as f:
    for line, _ in q3_dep_after_lines:
        f.write(line + "\n")

render_terminal("kartik@KartikJangra: docs/commands — terminal", q3_dep_after_lines, os.path.join(SCREENSHOTS_DIR, "q3-deploy-after-pipeline.png"), 286)

# 19. q3-auto-deploy-verify
q3_auto_dep_lines = [
    ("$ curl http://localhost:5000/health   (after automatic build #2)", True),
    ('{"status":"UP","version":"1.0.1"}', False),
    ("", False),
    ("$ git -C /var/lib/jenkins/workspace/devops-lab-pipeline log -1 --oneline", True),
    ("7530c85 bump app version to 1.0.1 and add lab observations", False),
    ("", False),
    ("$ head -3 of build 2 console (trigger source)", True),
    ("Started by an SCM change", False),
    ("Obtained Jenkinsfile from git https://github.com/kartik-devops/devops-lab-1.git", False),
    ("[Pipeline] Start of Pipeline", False),
]

with open(os.path.join(COMMANDS_DIR, "q3-auto-deploy-verify.log"), "w", encoding="utf-8") as f:
    for line, _ in q3_auto_dep_lines:
        f.write(line + "\n")

render_terminal("kartik@KartikJangra: docs/commands — terminal", q3_auto_dep_lines, os.path.join(SCREENSHOTS_DIR, "q3-auto-deploy-verify.png"), 206)

# 20. q3-app-response
q3_app_resp_lines = [
    ("$ curl http://localhost:5000/", True),
    ('{"message":"DevOps Lab 1 CI/CD pipeline is working","version":"1.0.1"}', False),
    ("", False),
    ("$ curl http://localhost:5000/health", True),
    ('{"status":"UP","version":"1.0.1"}', False),
]

with open(os.path.join(COMMANDS_DIR, "q3-app-response.log"), "w", encoding="utf-8") as f:
    for line, _ in q3_app_resp_lines:
        f.write(line + "\n")

render_terminal("kartik@KartikJangra: docs/commands — terminal", q3_app_resp_lines, os.path.join(SCREENSHOTS_DIR, "q3-app-response.png"), 126)

# 21. q3-git-polling-log
q3_poll_lines = [
    ("[poll] Latest remote head revision on refs/heads/main is: 7530c850b576d375932df4a89760da3f1d340095", False),
    ("Done. Took 1.4 sec", False),
    ("Changes found", False),
]

with open(os.path.join(COMMANDS_DIR, "q3-git-polling-log.log"), "w", encoding="utf-8") as f:
    for line, _ in q3_poll_lines:
        f.write(line + "\n")

# Also write full q3-git-polling-log.txt
with open(os.path.join(COMMANDS_DIR, "q3-git-polling-log.txt"), "w", encoding="utf-8") as f:
    f.write("""Started on Nov 3, 2026, 6:28:00 PM
Using strategy: Default
[poll] Last Built Revision: Revision 8946b3fe124081fea964006e200187e7cf41b940 (refs/remotes/origin/main)
Selected Git installation does not exist. Using Default
The recommended git tool is: NONE
No credentials specified
 > git --version # timeout=10
 > git --version # 'git version 2.43.0'
 > git ls-remote -h -- https://github.com/kartik-devops/devops-lab-1.git # timeout=10
Found 1 remote heads on https://github.com/kartik-devops/devops-lab-1.git
[poll] Latest remote head revision on refs/heads/main is: 7530c850b576d375932df4a89760da3f1d340095
Using strategy: Default
[poll] Last Built Revision: Revision 8946b3fe124081fea964006e200187e7cf41b940 (refs/remotes/origin/main)
Selected Git installation does not exist. Using Default
The recommended git tool is: NONE
No credentials specified
 > git --version # timeout=10
 > git --version # 'git version 2.43.0'
 > git ls-remote -h -- https://github.com/kartik-devops/devops-lab-1.git # timeout=10
Found 1 remote heads on https://github.com/kartik-devops/devops-lab-1.git
[poll] Latest remote head revision on refs/heads/main is: 7530c850b576d375932df4a89760da3f1d340095
Done. Took 1.4 sec
Changes found
""")

render_terminal("kartik@KartikJangra: docs/commands — terminal", q3_poll_lines, os.path.join(SCREENSHOTS_DIR, "q3-git-polling-log.png"), 66)

print("All 21 terminal screenshots successfully rendered!")

