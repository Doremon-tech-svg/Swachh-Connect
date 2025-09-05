import os
from flask import Flask, render_template, request, redirect, url_for, flash,send_from_directory

app = Flask(__name__)
app.secret_key = "supersecret"  # needed for flash messages

@app.route('/')
def home():
    return render_template('home.html')

# Training page
@app.route('/training')
def training():
    return render_template('training.html')


# Quiz page
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        score = 0
        if request.form.get('q1') == 'wet':
            score += 1
        if request.form.get('q2') == 'dry':
            score += 1
        if request.form.get('q3') == 'hazardous':
            score += 1

        if score >= 2:  # pass if 2/3 correct
            return render_template('certificate.html', score=score)
        else:
            return render_template('quiz.html', error="Try again!")
    return render_template('quiz.html')


# Make sure uploads folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB limit

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        description = request.form.get("description")
        location = request.form.get("location")
        file = request.files.get("photo")

        if not description or not location or not file:
            flash("⚠️ Please fill all fields and upload a photo.")
            return redirect(url_for("report"))

        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # For MVP, just flash success
            flash("✅ Report submitted successfully!")
            return redirect(url_for("uploads"))

        else:
            flash("⚠️ Invalid file format. Only images allowed.")
            return redirect(url_for("report"))

    return render_template("report.html")


@app.route("/uploads")
def uploads():
    # List files in uploads folder
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    # Prepare for rendering (only image files)
    images = [f for f in files if allowed_file(f)]
    return render_template("uploads.html", images=images)

# Serve uploaded files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)



@app.route("/dashboard")
def dashboard():
    # For MVP: count uploaded reports
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    images = [f for f in files if allowed_file(f)]
    report_count = len(images)

    # Dummy placeholders for now
    training_completed = True   # pretend the user has finished training
    certificate_earned = True   # pretend the user passed the quiz

    return render_template(
        "dashboard.html",
        report_count=report_count,
        training_completed=training_completed,
        certificate_earned=certificate_earned
    )



@app.route("/admin")
def admin():
    # Get list of uploaded reports (files only for now)
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    images = [f for f in files if allowed_file(f)]

    # Dummy data for now (will replace with DB later)
    training_completed = 25
    certificates_issued = 20
    reports_count = len(images)

    return render_template(
        "admin.html",
        reports=images,
        training_completed=training_completed,
        certificates_issued=certificates_issued,
        reports_count=reports_count
    )



if __name__ == "__main__":
    app.run(debug=True)
