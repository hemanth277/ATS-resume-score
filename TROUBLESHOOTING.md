# 🔍 Troubleshooting Guide - Resume Score Not Working

## Quick Diagnosis Steps

### Step 1: Test the Backend API

I've created a diagnostic test page for you. **Open this file in your browser:**

```
c:\Users\user\Desktop\ATS-Resume-Score\frontend\test-api.html
```

**What to do:**
1. Open `test-api.html` in your browser
2. Click each test button
3. Check if all tests pass ✅

**If tests fail:**
- Make sure the backend server is running (see Step 2)
- Check for CORS errors in browser console (F12)

---

### Step 2: Verify Backend Server is Running

**Check if the server is running:**
1. Look for a terminal/PowerShell window with this output:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

**If the server is NOT running, start it:**
```powershell
cd c:\Users\user\Desktop\ATS-Resume-Score\backend
uvicorn main:app --reload
```

**Keep this terminal window open!** The server must stay running while you use the application.

---

### Step 3: Check Browser Console for Errors

1. Open `index.html` in your browser
2. Press **F12** to open Developer Tools
3. Click the **Console** tab
4. Try uploading a resume and job description
5. Look for any **red error messages**

**Common errors and solutions:**

#### ❌ "Failed to fetch" or "Network Error"
**Cause:** Backend server not running or wrong URL

**Solution:**
- Make sure backend server is running (see Step 2)
- Check that `app.js` line 7 says: `const API_URL = 'http://localhost:8000';`

#### ❌ "CORS policy" error
**Cause:** Browser security blocking the request

**Solution:** This shouldn't happen with our setup, but if it does:
- Make sure you're opening the HTML file directly in the browser (not through a web server)
- Try a different browser (Chrome, Edge, Firefox)

#### ❌ "Only PDF files are supported"
**Cause:** You uploaded a non-PDF file

**Solution:** Make sure your resume is a PDF file

---

### Step 4: Check File Upload

**Make sure:**
- ✅ Your resume is a **PDF file** (not .docx, .txt, etc.)
- ✅ File size is **less than 10MB**
- ✅ You see a **green checkmark** after selecting the file
- ✅ Job description has **at least 10 characters**

---

### Step 5: Watch the Backend Logs

When you click "Analyze Resume", watch the backend terminal window. You should see:

```
INFO:     127.0.0.1:XXXXX - "POST /analyze HTTP/1.1" 200 OK
```

**If you see:**
- `200 OK` - Success! ✅
- `400 Bad Request` - Invalid file or job description
- `500 Internal Server Error` - Backend error (check terminal for details)
- **Nothing at all** - Request not reaching backend (connection issue)

---

## Common Issues and Solutions

### Issue 1: Nothing happens when clicking "Analyze Resume"

**Possible causes:**
1. JavaScript error preventing form submission
2. Backend server not running
3. Browser blocking the request

**Solutions:**
1. Check browser console (F12) for errors
2. Verify backend server is running
3. Try the test page (`test-api.html`)

---

### Issue 2: Loading animation shows but never completes

**Possible causes:**
1. Backend server crashed
2. Network timeout
3. Large PDF file taking too long

**Solutions:**
1. Check backend terminal for error messages
2. Try with a smaller PDF file
3. Restart the backend server

---

### Issue 3: Error message appears

**Read the error message carefully!** Common ones:

- "Only PDF files are supported" → Upload a PDF file
- "File size too large" → Use a smaller file (< 10MB)
- "Job description is too short" → Add more text (at least 10 characters)
- "Failed to analyze resume" → Check backend terminal for details

---

## Manual Test with Sample Data

If you don't have a PDF resume handy, here's how to test:

1. **Create a simple test PDF:**
   - Open any document in Word/Google Docs
   - Add some text like: "Software Engineer with Python, JavaScript, React experience"
   - Save/Export as PDF

2. **Use this sample job description:**
   ```
   We are looking for a Software Engineer with experience in Python, JavaScript, 
   and React. The ideal candidate will have strong problem-solving skills and 
   experience with modern web frameworks like FastAPI and Node.js. Knowledge of 
   databases, cloud technologies, and CI/CD pipelines is a plus.
   ```

3. **Upload and test**

---

## Still Not Working?

### Check These Files:

1. **Backend is running:** Terminal shows `Uvicorn running on http://127.0.0.1:8000`
2. **Frontend files exist:**
   - `c:\Users\user\Desktop\ATS-Resume-Score\frontend\index.html`
   - `c:\Users\user\Desktop\ATS-Resume-Score\frontend\app.js`
   - `c:\Users\user\Desktop\ATS-Resume-Score\frontend\app.css`

3. **Backend files exist:**
   - `c:\Users\user\Desktop\ATS-Resume-Score\backend\main.py`
   - `c:\Users\user\Desktop\ATS-Resume-Score\backend\ats.py`

### Get Detailed Error Information:

1. Open browser console (F12)
2. Go to **Network** tab
3. Try uploading a resume
4. Click on the `/analyze` request
5. Check the **Response** tab for error details

---

## Need More Help?

**Share this information:**
1. What error message do you see (if any)?
2. What does the browser console show (F12 → Console)?
3. What does the backend terminal show?
4. What happens when you run `test-api.html`?

This will help diagnose the exact issue!
