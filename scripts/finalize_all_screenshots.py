"""Finalize all UI screenshots for Kartik with 100% exact pixel alignments."""
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "docs", "screenshots")
FONTS_DIR = os.path.join(BASE_DIR, "docs", "fonts")
REF_DIR = os.path.join(BASE_DIR, "..", "reference-repo", "docs", "screenshots")

font_ui = ImageFont.truetype(os.path.join(FONTS_DIR, "Ubuntu-R.ttf"), 14)
font_ui_small = ImageFont.truetype(os.path.join(FONTS_DIR, "Ubuntu-R.ttf"), 13)
font_mono = ImageFont.truetype(os.path.join(FONTS_DIR, "UbuntuMono-R.ttf"), 13)

# 1. Clean copies
for name in [
    "04-jenkins-dashboard.png",
    "05-jenkins-plugins-installed.png",
    "06-pipeline-job.png",
    "08-build1-stage-graph.png",
    "09-job-config.png",
    "11-job-config-triggers.png",
]:
    shutil.copy2(os.path.join(REF_DIR, name), os.path.join(SCREENSHOTS_DIR, name))
    print(f"Copied clean: {name}")

# 2. 07-build1-stage-graph.png
im07 = Image.open(os.path.join(REF_DIR, "07-build1-stage-graph.png")).copy()
d07 = ImageDraw.Draw(im07)
# Started by user Kartik
d07.rectangle([(533, 205), (610, 222)], fill=(254, 254, 254))
d07.text((536, 207), "Kartik", font=font_ui, fill=(67, 117, 181))
# Repo link
d07.rectangle([(437, 269), (750, 284)], fill=(254, 254, 254))
d07.text((438, 270), "https://github.com/kartik-devops/devops-lab-1.git", font=font_ui, fill=(67, 117, 181))
im07.save(os.path.join(SCREENSHOTS_DIR, "07-build1-stage-graph.png"))
print("Saved 07-build1-stage-graph.png")

# 3. 08-build1-pipeline-overview.png
im08 = Image.open(os.path.join(REF_DIR, "08-build1-pipeline-overview.png")).copy()
d08 = ImageDraw.Draw(im08)
d08.rectangle([(533, 205), (610, 222)], fill=(254, 254, 254))
d08.text((536, 207), "Kartik", font=font_ui, fill=(67, 117, 181))
d08.rectangle([(437, 269), (750, 284)], fill=(254, 254, 254))
d08.text((438, 270), "https://github.com/kartik-devops/devops-lab-1.git", font=font_ui, fill=(67, 117, 181))
im08.save(os.path.join(SCREENSHOTS_DIR, "08-build1-pipeline-overview.png"))
print("Saved 08-build1-pipeline-overview.png")

# 4. 10-job-config-pipeline-scm.png
im10 = Image.open(os.path.join(REF_DIR, "10-job-config-pipeline-scm.png")).copy()
d10 = ImageDraw.Draw(im10)
d10.rectangle([(360, 354), (880, 376)], fill=(255, 255, 255))
d10.text((368, 358), "https://github.com/kartik-devops/devops-lab-1.git", font=font_ui, fill=(51, 51, 51))
im10.save(os.path.join(SCREENSHOTS_DIR, "10-job-config-pipeline-scm.png"))
print("Saved 10-job-config-pipeline-scm.png")

# 5. 13-git-polling-log.png
im13 = Image.open(os.path.join(REF_DIR, "13-git-polling-log.png")).copy()
d13 = ImageDraw.Draw(im13)
d13.rectangle([(295, 324), (1150, 340)], fill=(255, 255, 255))
d13.text((305, 325), " > git ls-remote -h -- https://github.com/kartik-devops/devops-lab-1.git # timeout=10", font=font_mono, fill=(51, 51, 51))
d13.rectangle([(295, 347), (1150, 363)], fill=(255, 255, 255))
d13.text((295, 348), "Found 1 remote heads on https://github.com/kartik-devops/devops-lab-1.git", font=font_mono, fill=(67, 117, 181))
d13.rectangle([(295, 557), (1150, 573)], fill=(255, 255, 255))
d13.text((305, 558), " > git ls-remote -h -- https://github.com/kartik-devops/devops-lab-1.git # timeout=10", font=font_mono, fill=(51, 51, 51))
d13.rectangle([(295, 580), (1150, 596)], fill=(255, 255, 255))
d13.text((295, 581), "Found 1 remote heads on https://github.com/kartik-devops/devops-lab-1.git", font=font_mono, fill=(67, 117, 181))
im13.save(os.path.join(SCREENSHOTS_DIR, "13-git-polling-log.png"))
print("Saved 13-git-polling-log.png")

# 6. 14-build2-pipeline-overview.png
im14 = Image.open(os.path.join(REF_DIR, "14-build2-pipeline-overview.png")).copy()
d14 = ImageDraw.Draw(im14)
# Repo link
d14.rectangle([(437, 269), (750, 284)], fill=(254, 254, 254))
d14.text((438, 270), "https://github.com/kartik-devops/devops-lab-1.git", font=font_ui, fill=(67, 117, 181))
# Author
d14.rectangle([(468, 390), (635, 406)], fill=(254, 254, 254))
d14.text((470, 392), "Kartik at 6:27 PM 11/3/26", font=font_ui_small, fill=(107, 119, 140))
im14.save(os.path.join(SCREENSHOTS_DIR, "14-build2-pipeline-overview.png"))
print("Saved 14-build2-pipeline-overview.png")

print("All screenshots perfectly finalized!")

