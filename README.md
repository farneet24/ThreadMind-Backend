# 🧠 ThreadMind Backend: Advanced Comment Analysis Service 📊

## 📌 Table of Contents
1. [👁‍🗨 Overview](#overview)
2. [✨ Features](#features)
3. [🛠 Technological Stack](#technological-stack)
4. [🌐 Usage](#try-now)
5. [⏳ Rate Limiting and Session Management](#rate-limiting-and-session-management)
6. [🤝 Contributing](#contributing)

## Overview

👋 Welcome to the official backend repository for **ThreadMind**, an intelligent service designed for in-depth analysis of comments from YouTube and Reddit platforms. 📈 This system incorporates state-of-the-art machine learning algorithms 🤖 to perform sentiment analysis, emotion recognition, and cyberbullying classification. 📚 It also offers comment summarization and keyword extraction capabilities.

## Features 

### 📊 Data Aggregation
- 📌 **What it does**: Gathers contextual information such as the post/video description, channel/subreddit details, and audience engagement metrics.
- 📘 **How it works**: Utilizes OAuth 2.0 protocols to securely interface with YouTube and Reddit APIs and fetch relevant metadata. 

### 🗨️ Comment Analytics
- 📈 **What it does**: Delivers insightful analytics including sentiment distribution, emotional tendencies, and cyberbullying flags for user comments.
- 📘 **How it works**: Leverages custom-tailored language models that have been fine-tuned on specialized datasets harvested from social media platforms such as Twitter and Reddit. These models are optimized for high-accuracy text analytics, enabling nuanced understanding of user-generated content. For diving deeper into the technical aspects, the Jupyter notebooks detailing our data processing and model fine-tuning workflows are available [here](https://github.com/farneet24/Pre-trained-Models.git).
 
### 📝 NLP-powered Summarization
- 🤖 **What it does**: Summarizes lengthy comment threads and extracts keywords for quick understanding.
- 📘 **How it works**: Implement OpenAI's GPT-3.5TURBO for generating concise and informative summaries and for keyword extraction, using techniques like Term Frequency-Inverse Document Frequency (TF-IDF).

## 🛠 Technological Stack

- 🗨️ **Communication**: REST API — A standard for creating scalable and stateless services.
- 🚀 **Deployment Platform**: Heroku — A cloud-based service that enables quick and hassle-free deployment.
- 📊 **Data Sources**: YouTube API, Reddit API — Provide the raw data that fuels our analytics.
- 🤖 **Machine Learning Models**: OpenAI GPT-3.5TURBO, Fine-tuned RoBERTa and XLNet hosted on Google Cloud Run — These are the core algorithms responsible for the project's advanced analytics capabilities.

## Try Now

👉 Access the website by clicking on this link, [ThreadMind](https://thread-mind.vercel.app/).

## Rate Limiting and Session Management

- 🕒 Rate-limiting mechanisms are implemented to control the frequency of API requests.
- 🔒 Unique session IDs are generated to optimize resource allocation and prevent redundant queries.

## Contributing

🙌 Contributions are welcome! If you're interested in collaborating or contributing, feel free to connect with me here on [LinkedIn](https://www.linkedin.com/in/farneet-singh-6b155b208/)!

