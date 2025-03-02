from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import sqlite3
import csv

app = Flask(__name__)

# Connexion à la base de données pour stocker l'historique
conn = sqlite3.connect("seo_history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS history (keyword TEXT, position INTEGER, date TEXT)")
conn.commit()

def get_google_rank(keyword, site_url):
    headers = {"User-Agent": "Mozilla/5.0"}
        search_url = f"https://www.google.com/search?q={keyword}&num=100"
            response = requests.get(search_url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")
                    
                        results = soup.find_all("div", class_="tF2Cxc")
                            for index, result in enumerate(results, start=1):
                                    link = result.find("a")["href"]
                                            if site_url in link:
                                                        return index  
                                                            return None  

                                                            @app.route("/check", methods=["GET"])
                                                            def check_seo():
                                                                keyword = request.args.get("keyword")
                                                                    site_url = request.args.get("site")
                                                                        if not keyword or not site_url:
                                                                                return jsonify({"error": "Veuillez fournir un mot-clé et un site"}), 400

                                                                                    position = get_google_rank(keyword, site_url)

                                                                                        if position:
                                                                                                cursor.execute("INSERT INTO history VALUES (?, ?, datetime('now'))", (keyword, position))
                                                                                                        conn.commit()
                                                                                                                return jsonify({"keyword": keyword, "position": position})
                                                                                                                    else:
                                                                                                                            return jsonify({"message": "Site non trouvé dans le top 100"}), 404

                                                                                                                            @app.route("/history", methods=["GET"])
                                                                                                                            def get_history():
                                                                                                                                cursor.execute("SELECT * FROM history ORDER BY date DESC")
                                                                                                                                    data = cursor.fetchall()
                                                                                                                                        return jsonify(data)

                                                                                                                                        @app.route("/export", methods=["GET"])
                                                                                                                                        def export_data():
                                                                                                                                            cursor.execute("SELECT * FROM history")
                                                                                                                                                data = cursor.fetchall()

                                                                                                                                                    with open("seo_history.csv", "w", newline="") as f:
                                                                                                                                                            writer = csv.writer(f)
                                                                                                                                                                    writer.writerow(["Keyword", "Position", "Date"])
                                                                                                                                                                            writer.writerows(data)

                                                                                                                                                                                return jsonify({"message": "Fichier CSV généré"}), 200

                                                                                                                                                                                if __name__ == "__main__":
                                                                                                                                                                                    app.run(host="0.0.0.0", port=5000)