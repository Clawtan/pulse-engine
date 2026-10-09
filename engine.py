import json
import os
import random
import subprocess
import time
from datetime import datetime, timezone

def run():
    is_manual = os.getenv("GITHUB_EVENT_NAME") == "workflow_dispatch"
    now = datetime.now(timezone.utc)
    weekday = now.weekday()
    
    # Stochastic rest probability for realistic human distribution
    if not is_manual:
        threshold = 0.65 if weekday >= 5 else 0.85
        if random.random() > threshold:
            print("[INFO] Stochastic rest interval triggered. Skipping pulse for natural distribution.")
            return

    # Random commit batch size: 1 to 3 pulses per run
    weights = [50, 35, 15]
    num_commits = random.choices([1, 2, 3], weights=weights)[0]
    if is_manual:
        num_commits = max(1, num_commits)

    print(f"[INFO] Generating {num_commits} stochastic telemetry pulse(s)...")

    file_path = "data/heartbeat.json"
    commit_actions = [
        "record node heartbeat checkpoint",
        "synchronize telemetry pulse state",
        "update health monitor metrics",
        "log runtime diagnostic state",
        "persist node uptime verification"
    ]

    for i in range(num_commits):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"total_pulses": 0}
        
        current_ts = datetime.now(timezone.utc).isoformat()
        data["last_pulse"] = current_ts
        data["status"] = "healthy"
        data["node_id"] = "pulse-node-01"
        data["total_pulses"] = data.get("total_pulses", 0) + 1
        data["telemetry"] = {
            "latency_ms": round(random.uniform(9.0, 24.5), 1),
            "memory_pressure": random.choice(["nominal", "optimal", "balanced"])
        }
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
            
        subprocess.run(["git", "add", file_path], check=True)
        msg = f"chore(telemetry): {random.choice(commit_actions)} [skip ci]"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        print(f"[SUCCESS] Recorded commit {i + 1}/{num_commits}: {msg}")
        
        if i < num_commits - 1:
            time.sleep(random.randint(2, 4))

    print("[SUCCESS] All telemetry pulses committed successfully.")

if __name__ == "__main__":
    run()
