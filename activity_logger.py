from datetime import datetime

def log_activity(action_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {action_message}\n"
    
    with open("audit_log.txt", mode="a", encoding="utf-8") as f:
        f.write(log_line)