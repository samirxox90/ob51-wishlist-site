from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

REGIONS = {
    "Global": "sg",
    "Brazil / USA / NA": "br",
    "India": "ind"
}

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    success = False

    if request.method == "POST":
        uid = request.form.get("uid")
        password = request.form.get("password")
        itemid = request.form.get("itemid")
        region_name = request.form.get("region")
        action = request.form.get("action")

        if not uid or not password:
            message = "❌ Please enter UID and Password."
        elif not itemid or not itemid.isdigit():
            message = "❌ Please enter a valid numeric Item ID."
        elif not region_name:
            message = "❌ Please choose a region."
        elif not action:
            message = "❌ Please choose an action (Add or Remove)."
        else:
            region = REGIONS.get(region_name)
            api_url = f"https://ob51wishlist-untuk-cintaku.vercel.app/api/{action}/{itemid}/{region}/{uid}/{password}"

            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get("status") == "success":
                            message = f"✅ Success! Item {itemid} {action}ed successfully."
                            success = True
                        else:
                            message = "⚠️ Unexpected response — maybe wrong region or forbidden item"
                    except json.JSONDecodeError:
                        message = "✅ Success! Action completed."
                        success = True
                elif response.status_code == 404:
                    message = "⚠️ Item ID or region not found."
                elif response.status_code == 401:
                    message = "⚠️ Invalid UID or password."
                elif response.status_code >= 500:
                    message = "⚠️ Server error — please try again later."
                else:
                    message = f"⚠️ Error {response.status_code} — maybe wrong region or forbidden item"
            except Exception:
                message = "❌ Network error — please check your internet connection."

    return render_template("index.html", regions=REGIONS.keys(), message=message, success=success)
    

if __name__ == "__main__":
    app.run(debug=True)
