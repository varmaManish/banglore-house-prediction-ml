from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import pickle
import numpy as np
import os

load_dotenv()  # loads variables from .env file automatically

app = Flask(__name__)

# ─── SECRET KEY (required for flash messages) ────────────────────────────────
app.secret_key = os.environ.get('SECRET_KEY', 'houseai-secret-2026')

# ─── FLASK-MAIL CONFIG (Gmail SMTP) ──────────────────────────────────────────
app.config['MAIL_SERVER']         = 'smtp.gmail.com'
app.config['MAIL_PORT']           = 587
app.config['MAIL_USE_TLS']        = True
app.config['MAIL_USE_SSL']        = False
app.config['MAIL_USERNAME']       = os.environ.get('MAIL_USER', 'mv918038@gmail.com')
app.config['MAIL_PASSWORD']       = os.environ.get('MAIL_PASS', '')   # set via env var
app.config['MAIL_DEFAULT_SENDER'] = ('HouseAI System', os.environ.get('MAIL_USER', 'mv918038@gmail.com'))

mail = Mail(app)

# ─── LOAD MODEL & LABEL ENCODER ──────────────────────────────────────────────
model = pickle.load(open('price_model.pkl', 'rb'))
le    = pickle.load(open('label_encoder.pkl', 'rb'))
locations = sorted(le.classes_.tolist())
print("LOCATIONS:", locations[:5])  # Debug print


# ─── HOME ─────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html', locations=locations, prediction_text=None)


# ─── PREDICT ──────────────────────────────────────────────────────────────────
@app.route('/predict', methods=['POST'])
def predict():
    try:
        location    = request.form['location']
        total_sqft  = float(request.form['sqft'])
        bath        = int(request.form['bath'])
        bhk         = int(request.form['bhk'])

        location_encoded = le.transform([location])[0]
        features         = np.array([[total_sqft, bath, bhk, location_encoded]])
        predicted_price  = model.predict(features)[0]

        return render_template(
            'index.html',
            locations=locations,
            prediction_text=f"Estimated Price: ₹ {predicted_price:.2f} Lakhs",
            location_text=f"Location: {location}"
        )
    except Exception as e:
        return render_template(
            'index.html',
            locations=locations,
            prediction_text="Prediction failed. Please check your input.",
            location_text=f"Error: {str(e)}"
        )


# ─── TEST ROUTE ───────────────────────────────────────────────────────────────
@app.route('/test')
def test_template():
    test_locations = ['Location1', 'Location2', 'Location3']
    return render_template('index.html',
                           locations=test_locations,
                           prediction_text="Test Prediction",
                           location_text="Test Location")


# ─── ABOUT ────────────────────────────────────────────────────────────────────
@app.route('/about')
def about():
    return render_template('about.html')


# ─── STATS ────────────────────────────────────────────────────────────────────
@app.route('/stats')
def stats():
    return render_template('stats.html')


# ─── CONTACT (GET + POST) ─────────────────────────────────────────────────────
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name    = request.form.get('name',    '').strip()
        email   = request.form.get('email',   '').strip()
        phone   = request.form.get('phone',   '').strip()
        subject = request.form.get('subject', 'General Inquiry').strip()
        message = request.form.get('message', '').strip()

        # Basic validation
        if not name or not email or not phone:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('contact'))

        # ── HTML email body ───────────────────────────────────────────────────
        html_body = f"""
        <html>
        <body style="font-family:Arial,sans-serif; background:#0a0f1e; color:#e0f0ff; padding:30px; margin:0;">
          <div style="max-width:600px; margin:0 auto; background:#050d1a;
                      border:1px solid rgba(0,245,255,0.2); border-radius:6px; overflow:hidden;">

            <!-- Header -->
            <div style="background:#000d1f; padding:20px 30px; border-bottom:1px solid rgba(0,245,255,0.15);">
              <h1 style="font-family:'Courier New',monospace; color:#00f5ff; margin:0;
                         font-size:1.3rem; letter-spacing:4px;">
                ⬡ HOUSEAI — NEW INQUIRY
              </h1>
            </div>

            <!-- Fields -->
            <div style="padding:30px;">
              <table style="width:100%; border-collapse:collapse;">
                <tr>
                  <td style="padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.06);
                             color:#00f5ff; font-family:'Courier New',monospace;
                             font-size:0.72rem; letter-spacing:2px; width:120px; vertical-align:top;">NAME</td>
                  <td style="padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.06);
                             color:#e0f0ff; font-size:1rem;">{name}</td>
                </tr>
                <tr>
                  <td style="padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.06);
                             color:#00f5ff; font-family:'Courier New',monospace;
                             font-size:0.72rem; letter-spacing:2px; vertical-align:top;">EMAIL</td>
                  <td style="padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:1rem;">
                    <a href="mailto:{email}" style="color:#00f5ff; text-decoration:none;">{email}</a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.06);
                             color:#00f5ff; font-family:'Courier New',monospace;
                             font-size:0.72rem; letter-spacing:2px; vertical-align:top;">PHONE</td>
                  <td style="padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.06);
                             color:#00ff88; font-family:'Courier New',monospace; font-size:1rem;">
                    <a href="tel:{phone}" style="color:#00ff88; text-decoration:none;">{phone}</a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.06);
                             color:#00f5ff; font-family:'Courier New',monospace;
                             font-size:0.72rem; letter-spacing:2px; vertical-align:top;">SUBJECT</td>
                  <td style="padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.06);
                             color:#ffd700; font-size:1rem;">{subject}</td>
                </tr>
              </table>

              <!-- Message block -->
              <div style="margin-top:24px;">
                <div style="color:#00f5ff; font-family:'Courier New',monospace;
                           font-size:0.72rem; letter-spacing:2px; margin-bottom:10px;">MESSAGE</div>
                <div style="background:#000d1f; border-left:3px solid #00f5ff;
                           padding:16px 20px; color:#b4d2ff; font-size:0.95rem;
                           line-height:1.7; border-radius:0 4px 4px 0;">
                  {message if message else '<em style="opacity:0.5">No message provided.</em>'}
                </div>
              </div>

              <!-- Quick reply button -->
              <div style="margin-top:28px; text-align:center;">
                <a href="mailto:{email}?subject=Re: {subject}"
                   style="display:inline-block; padding:12px 32px;
                          background:transparent; border:1px solid #00f5ff;
                          color:#00f5ff; font-family:'Courier New',monospace;
                          font-size:0.75rem; letter-spacing:3px; text-decoration:none;
                          border-radius:2px;">
                  ◈ REPLY TO {name.upper()}
                </a>
              </div>
            </div>

            <!-- Footer -->
            <div style="background:#000d1f; padding:14px 30px;
                        border-top:1px solid rgba(0,245,255,0.1); text-align:center;">
              <span style="font-family:'Courier New',monospace; font-size:0.6rem;
                           color:rgba(255,255,255,0.2); letter-spacing:3px;">
                © 2026 HOUSEAI SYSTEM — AUTO-GENERATED NOTIFICATION
              </span>
            </div>
          </div>
        </body>
        </html>
        """

        try:
            msg = Message(
                subject=f'[HouseAI] {subject} — from {name}',
                recipients=['mv918038@gmail.com'],
                reply_to=email,
                html=html_body
            )
            mail.send(msg)
            flash(f'Message sent! We will reach you at {email} or {phone} within 24 hours.', 'success')

        except Exception as e:
            print(f'[MAIL ERROR] {e}')
            flash('Transmission failed. Please try again or email us directly at mv918038@gmail.com.', 'error')

        return redirect(url_for('contact'))

    # GET — just render the form
    return render_template('contact.html')


# ─── RUN ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)