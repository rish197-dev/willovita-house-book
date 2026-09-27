# Willovita House Book

Proof-of-concept front end for running the Willovita guest houses: owner dashboard, coordinator calendar and stay requests, crew views by role, house guides, events and waiver tracking, categorized repairs, a private guest link, and an in-house iPad view.

- Single static page, no build step, hosted on GitHub Pages.
- Data is sample data held in memory. Nothing is saved; a reload resets it.

## How the password works

`index.html` holds only a login page and the app encrypted with AES-256-GCM. The key comes from the password (PBKDF2-SHA256, 600,000 rounds), and the page decrypts itself in the browser after the right password is entered. Without the password, the repo and the live site show nothing but ciphertext. Unlocking lasts for the browser session.

The protection is only as good as the password. Share it privately, never in this repo, an issue, or a commit message.

## Updating the app or changing the password

The readable app (`app.html`) is kept outside the repo and listed in `.gitignore`.

```
pip install cryptography
python3 tools/encrypt.py app.html "the-pass-phrase"
git commit -am "Update House Book" && git push
```

Run the same command with a new pass phrase to change the password. Everyone who is logged in stays in until they close the browser.
