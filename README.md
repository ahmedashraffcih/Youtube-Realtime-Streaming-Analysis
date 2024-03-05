# Youtube Realtime Streaming Analysis

## 🪄 Introduction


This project, built using Python, is designed to retrieve up-to-the-minute YouTube statistics such as likes, views, comments, and favorites. 
It streams this data through Kafka. Additionally, KSqlDB is utilized for stream processing, after which the processed data is forwarded to a Telegram bot to provide real-time notifications.

## System Architecture

![System Architecture](https://github.com/ahmedashraffcih/Youtube-Realtime-Streaming-Analysis/tree/main/assets/architecture.png)

## Requirements

- **Python**
- **Kafka**
- **Youtube API**
- **Telegram API**
- **Docker**
- **Confluent Containers (Zookeeper, Kafka, Schema Registry, Connect, ksqlDB, Control Center)**
---

## How It works

- Retrieves data from YouTube API by utilizing the provided playlist ID.
- - For example I used Garage Education - Hadoop & Distributed Systems Playlist
- Transmits the obtained data to Kafka.
- Incorporates an additional component (not detailed here but discussed in the video) that reads from the Kafka topic and conducts real-time analytics - using ksqlDB.
- The outcomes of the analytics are then dispatched to Telegram for instantaneous notifications.

---


## 💿 Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/ahmedashraffcih/Youtube-Realtime-Streaming-Analysis.git
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Open `config/config.local` and set the following:
    - `API_KEY`: Your YouTube API Key
    - `PLAYLIST_ID`: The YouTube playlist ID you want to track

4. Set up your Kafka server address in the main script, by default, it's set to `localhost:9092`.

5. Start your Kafka and other Confluent services on Docker with
   ```bash
   docker compose up -d
   ``` 

6. Run the Python script.
    ```bash
    python analytics.py
    ```
---


## ✨ Contribution

Contributions and feedback are welcome! If you have any ideas, suggestions, or improvements, feel free to open an issue or submit a pull request.


To contribute to this project, see the GitHub documentation on **[creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)**.

---

## 👏 Support

Give a ⭐️ if you like this project!
___________________________________

<p>&copy; 2024 Ahmed Ashraf</p>

