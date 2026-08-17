# Bhoomika's Birthday Countdown Automation 🎂

Sends her a mystery countdown email every midnight (IST) until Sept 23,
with a link to a live countdown + "guess who" mini-game page.

## What's inside
- `send_email.py` — picks a message, calculates days remaining, sends via Gmail
- `.github/workflows/nightly-email.yml` — runs the script automatically every night, for free, on GitHub's servers
- `docs/index.html` — the live countdown + guess-the-nickname page (3 tries/day), hosted on GitHub Pages

## One-time setup (about 10 minutes)

### 1. Create the repo
- Go to github.com → New repository (can be **private**)
- Upload all files from this folder, keeping the same structure (the `.github` folder must stay at the root)

### 2. Get a Gmail App Password
Regular Gmail passwords won't work for this — you need an "app password":
1. Go to https://myaccount.google.com/security
2. Turn on **2-Step Verification** if it isn't already on
3. Search "App Passwords" in your Google Account settings
4. Generate one (name it "birthday bot"), copy the 16-character code

### 3. Add secrets to your repo
In your repo → **Settings → Secrets and variables → Actions → New repository secret**, add:
| Name | Value |
|---|---|
| `GMAIL_USER` | your Gmail address |
| `GMAIL_APP_PASSWORD` | the 16-character app password from step 2 |
| `GUESS_PAGE_URL` | your GitHub Pages URL — see step 4 (add this after step 4) |

### 4. Enable GitHub Pages
- Repo → **Settings → Pages**
- Source: **Deploy from a branch**
- Branch: `main`, folder: `/docs`
- Save. Your live page will be at:
  `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`
- Copy that URL and add it as the `GUESS_PAGE_URL` secret (step 3)

### 5. Test it
- Repo → **Actions** tab → "Nightly Birthday Countdown Email" → **Run workflow** (manual trigger)
- Check her inbox — if it lands, you're all set

### 6. Let it run
It fires automatically every night at 00:00 IST until Sept 23. After her
birthday, the script detects the date has passed and stops sending on its own
— no need to delete anything, though you're welcome to archive the repo after.

## Customizing
- Edit the `MESSAGES` list in `send_email.py` to add your own lines
- Edit `docs/index.html` to change colors, wording, or the hint text
- The answer to the guessing game is set in `docs/index.html` as `const ANSWER = "bhaiya";`

## Notes
- Cron time is set for IST (UTC+5:30). If you're not in India, adjust the
  `cron:` line in `.github/workflows/nightly-email.yml` — GitHub Actions
  cron syntax is always in UTC.
- GitHub Actions free tier easily covers one email a night — no cost.
