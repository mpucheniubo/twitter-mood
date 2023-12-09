# 📊 Twitter Mood

This is a quick and small timer trigger application to calculate the mood from tweets that runs as an Azure function and uses the Python library `AFINN` for sentiment analysis.

## ⚙️ Functionality

The functino retrieves periodically tweets from the database and runs sentiment analysis on the content. Then it inserts the result in a differnet table linking the values with the original tweet via the ID.

The sentiments are not normalized, so that they can be compared across different iterations.

## 📜 Notes

This was part of a larger project that never went into production, so a cleaner implementation with a more TDD approach won't happen.

The project is being made public without the git history.