# 🧠 ThreadMind Backend: Advanced Comment Analysis Service 📊

## 📌 Table of Contents
1. [👁‍🗨 Overview](#overview)
2. [✨ Features](#features)
3. [🛠 Technological Stack](#technological-stack)
4. [🌐 Usage](#try-now)
5. [⏳ Rate Limiting and Session Management](#rate-limiting-and-session-management)
6. [🤝 Contributing](#contributing)

## 👁‍🗨 Overview

Welcome to the backend repository of **ThreadMind**, a pioneering service specialized in the sophisticated analysis of user-generated content on YouTube and Reddit platforms. This repository serves as the backbone for the application, employing state-of-the-art machine learning algorithms for sentiment analysis, emotion recognition, and cyberbullying classification, along with natural language summarization and keyword extraction capabilities.

## ✨ Features

### 📊 Data Aggregation
- **Objective**: To accrue and amalgamate a spectrum of contextual metadata, including channel/subreddit attributes and post/video descriptions.
- **Implementation**: Utilizes OAuth 2.0 protocols for secure API calls to YouTube and Reddit, ensuring data integrity and security.

### 🗨️ Comment Analytics
- **Objective**: To offer actionable insights by performing sentiment analysis, emotion recognition, and cyberbullying classification on user comments.
- **Implementation**: Employs fine-tuned machine learning models on socially-sourced datasets, including but not limited to Twitter and Reddit. For an in-depth review of the models and methodologies, refer to the associated [Jupyter notebooks](https://github.com/farneet24/Pre-trained-Models.git).

### 📝 NLP-powered Summarization
- **Objective**: To distill extensive comment threads into concise summaries and relevant keywords.
- **Implementation**: Leverages the capabilities of OpenAI's GPT-3.5TURBO model, utilizing advanced NLP techniques like TF-IDF for keyword extraction.

## 🛠 Technological Stack

- **Communication**: REST API
- **Deployment Platform**: Heroku
- **Data Sources**: YouTube API, Reddit API
- **Machine Learning Models**: OpenAI GPT-3.5TURBO, Fine-tuned RoBERTa, and XLNet hosted on Google Cloud Run

## 🌐 Usage

Experience the live application [here](https://thread-mind.vercel.app/).

## ⏳ Rate Limiting and Session Management

- **Rate Limiting**: Implemented to manage the API request frequency, thereby ensuring system stability.
- **Session Management**: Unique session IDs are generated to optimize resource allocation and to circumvent redundancy.

## 🤝 Contributing

Interested contributors are invited to connect via [LinkedIn](https://www.linkedin.com/in/farneet-singh-6b155b208/).


## Contributing

🙌 Contributions are welcome! If you're interested in collaborating or contributing, feel free to connect with me here on [LinkedIn](https://www.linkedin.com/in/farneet-singh-6b155b208/)!

