from __future__ import annotations

import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

from config import Settings
from formatters.report_formatter import telegram_text
from services import build_investigator

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to Hermes Chain Detective. Use /help to see commands.")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Commands:\n"
        "/investigate <address>\n"
        "/explain <address>\n"
        "/compare <address1> <address2>"
    )


async def investigate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /investigate <address>")
        return
    addr = context.args[0]
    investigator = build_investigator()
    result = investigator.run(addr, mode="investigate")
    await update.message.reply_text(telegram_text(result.report), parse_mode=ParseMode.MARKDOWN)


async def explain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /explain <address>")
        return
    addr = context.args[0]
    investigator = build_investigator()
    result = investigator.run(addr, mode="explain")
    await update.message.reply_text(telegram_text(result.report), parse_mode=ParseMode.MARKDOWN)


async def compare(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /compare <address1> <address2>")
        return
    investigator = build_investigator()
    result = investigator.run(context.args[0], mode="compare", address2=context.args[1])
    await update.message.reply_text(telegram_text(result.report), parse_mode=ParseMode.MARKDOWN)


def run_bot() -> None:
    settings = Settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing in environment")

    app = Application.builder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("investigate", investigate))
    app.add_handler(CommandHandler("explain", explain))
    app.add_handler(CommandHandler("compare", compare))

    logger.info("Starting Hermes Chain Detective Telegram bot...")
    app.run_polling()
