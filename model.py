def predict_risk(heart_rate, bp, oxygen):
    if heart_rate > 100 or bp > 140 or oxygen < 90:
        return "High Risk"
    else:
        return "Normal"