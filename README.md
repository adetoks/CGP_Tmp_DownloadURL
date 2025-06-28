# Read me
### 1. Fix the prompt

Make sure your command is entered all on one line, with matching quotes. For example:

```bash
curl -C - --output my_export.zip "https://your.export.url/that/file.zip"
```

Once you hit **Enter** on that complete line, you’ll get back to your normal prompt (e.g. `bash-3.2$`) and curl will start downloading.

---

### 2. Watching the download 

By default, curl will show you a live progress meter like this:

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  
  5 1024M    5  50.0M    0     0   500k      0  0:35:00 0:01:42 0:33:18  600k
```

If you prefer a simpler progress bar, add `-#`:

```bash
curl -C - -# --output my_export.zip "https://…"
```

---

### 3. Verifying it’s running

* **In the same window** you’ll see the meter updating every second—if it’s moving, it’s downloading.
* **In a separate tab/window**, run:

  ```bash
  ps aux | grep curl
  ```

  If you see your curl command listed, it’s still active.
* **Or watch the file grow**:

  ```bash
  watch -n1 ls -lh my_export.zip
  ```

  (Press Ctrl-C to stop watching.)

---

