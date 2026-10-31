# NEXORA AI — Full Windows Project

An English-first Discord AI bot with multilingual chat, image understanding, image generation, configurable reasoning effort, optional Google Search grounding, per-user chat history, daily usage limits, and a channel-based chat mode.

## Included features

- Normal chat in one configured text channel.
- Mention `@NEXORA AI` in other text channels to ask a question.
- `/ask` for normal AI chat.
- `/think` with low / medium / high reasoning effort.
- `/imagine` for AI image generation.
- Image understanding: attach an image in the configured chat channel or with a bot mention.
- `/search` for Google Search-grounded answers (disabled by default).
- `/resetme` to clear your saved chat history.
- `/setchat` lets a server manager choose the chat channel from Discord.
- `/status` and `/help`.
- SQLite conversation history.
- Daily request limit for other users; an optional owner ID bypasses the bot's app-level daily limit.
- English, Sinhala, and other languages supported by the selected Gemini model.

## Important limitations

1. No code can guarantee every feature works for every account before it is tested. Google model availability, API quotas, billing, Discord permissions, and package/API changes can affect features.
2. Image generation requires access to the configured image model (`IMAGE_MODEL`). If your Google AI project does not have access, `/imagine` will return an error; check the model availability in Google AI Studio.
3. Google Search grounding is off by default because it can consume quota and may incur charges. Review current Google AI pricing before enabling it.
4. High reasoning can take longer and use more tokens. This starter configuration uses Gemini 2.5 Flash thinking budgets.
5. The owner bypass only bypasses this bot's own daily limit. It does **not** bypass Google API quotas, provider rate limits, or billing.
6. This is a single-process starter project, not yet a production SaaS subscription platform. Before inviting it widely, add monitoring, stronger per-server quotas, abuse protection, and secure hosting.

## Step 1 — Install Python

Install Python 3.11 for Windows from:
https://www.python.org/downloads/

During setup, tick **Add python.exe to PATH**. You do not need to connect your phone to your PC.

Open Command Prompt and check:
```bat
py -3.11 --version
```

## Step 2 — Extract and open the project

1. Download the ZIP and choose **Extract All**.
2. Open VS Code.
3. Choose **File → Open Folder** and select the extracted `NEXORA_AI_Full` folder.
4. Open the terminal in VS Code using **Terminal → New Terminal**.

## Step 3 — Create your Discord bot

1. Open the Discord Developer Portal: https://discord.com/developers/applications
2. Create an application, then open its **Bot** page and create the bot user.
3. Copy the bot token and keep it private.
4. Under **Bot → Privileged Gateway Intents**, enable **Message Content Intent**.
5. Under **OAuth2 → URL Generator**, select scopes `bot` and `applications.commands`.
6. Select permissions: View Channels, Send Messages, Read Message History, Attach Files, Use Slash Commands.
7. Open the generated invite link and add the bot to your server.

Never paste your Discord token into chat or share it with anyone.

## Step 4 — Get a Gemini API key

Open Google AI Studio:
https://aistudio.google.com/

Create an API key and keep it private. Availability, quotas, and billing terms depend on Google's current rules and your project.

## Step 5 — Install packages

Run `setup.bat` by double-clicking it, or in VS Code terminal:
```powershell
.\setup.bat
```
The script creates `.venv`, installs packages, and creates `.env` if it doesn't exist.

## Step 6 — Configure `.env`

Open `.env` in VS Code. Replace the placeholder values:
- `DISCORD_TOKEN`
- `GEMINI_API_KEY`

For your own unlimited bot-level usage:
1. In Discord, enable Developer Mode under User Settings → Advanced.
2. Right-click your own user profile and copy your User ID.
3. Put it in `OWNER_USER_ID`.

This only bypasses the bot's daily limit for that user. It does not make Gemini API usage free or unlimited.

## Step 7 — Start the bot

Double-click `start.bat`, or run:
```powershell
.\start.bat
```
Keep the terminal window open while you use the bot.

## Step 8 — Choose the chat channel

In your Discord server, run `/setchat` and choose your AI chat channel. You need **Manage Server** permission. This saves the channel ID to your local `.env` file.

You can now:
- Talk normally in that channel.
- Mention `@NEXORA AI` in other channels.
- Use `/ask`, `/think`, `/imagine`, `/search`, `/help`, `/status`, and `/resetme`.

## Optional: enable Google Search grounding

Only after reviewing the current Google AI pricing/model support, change:
```env
ENABLE_GOOGLE_SEARCH=true
```
Then restart the bot.

## Troubleshooting

- **Invalid Discord token:** reset/copy the bot token in the Developer Portal and update `.env`.
- **Message channel doesn't respond:** confirm Message Content Intent is enabled in the Developer Portal, restart the bot, then use `/setchat`.
- **Slash commands missing:** wait a short time, check the terminal for sync errors, and make sure the invite included `applications.commands`.
- **Image generation fails:** check `IMAGE_MODEL`, your Google AI project access, quota, and billing settings.
- **AI model error:** verify `GEMINI_MODEL` is available to your API project and check the terminal log.
- **Module not found:** rerun `setup.bat`.
- **Do not share** your `.env` file or screenshots containing tokens.

## Privacy note

The bot stores chat text in a local SQLite database on the computer where it runs. `/resetme` deletes the user's saved chat history from that database. Image attachments are sent to the configured Gemini API for analysis; do not upload private images or sensitive data unless you understand the provider's terms.
