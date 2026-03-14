---

# PUBG Artillery/Mortar Distance Calculator

A lightweight Python utility designed to help players calculate precise artillery distances in PUBG. By calibrating to the in-game grid, the tool provides accurate measurements from your current position to your target.


<table>
<tr>
   <td><b>Support Project</b></td>
   <td >
      <a href="https://www.paypal.com/donate/?hosted_button_id=7QQS473KE8C38"><img src="https://raw.githubusercontent.com/seerge/g-helper/main/docs/paypal-eur.png" width="150" alt="PayPal EUR"></a>&nbsp;
      <a href="https://www.paypal.com/donate/?hosted_button_id=SXNDJMPSYW4CQ"><img src="https://raw.githubusercontent.com/seerge/g-helper/main/docs/paypal-usd.png" width="150" alt="PayPal USD"></a>&nbsp;
   </td>
</tr>
</table>

---

## 📸 Video Example (might be added soon, you can send me yours)

</br>

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/video_example.jpg)

</br>

---

## 🚀 Installation

### .exe usage

1. **Download the App**: Navigate to the [Releases](https://github.com/Yehor4k/pubg/releases/) tab and download the latest version of the executable.

2. Navigate to your Downloads folder and execute the calc.exe file.

### .py usage, aka source code

1. Install [Git](https://git-scm.com/install/windows) on your computer (optional) | Or just download the source code. Click green "<> Code" button at the top and download the .zip file | [Follow this tutorial on how to download the source code](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives#downloading-source-code-archives)

2. Install Python and in cmd install the pynput library with this command:
```bash
pip install pynput

```

3. (Follow this step only, if you installed the Git) Open your prefferable folder and copy the repository with Git via cmd:
```bash
git clone https://github.com/Yehor4k/pubg

```
Then open the cloned repository folder via this command:
```bash
cd pubg

```

4. Execute the run.py file with this command after you installed the pynput library:
```bash
py run.py

```

---

## 🛡️ The Windows Defender issue

### In case of a single .exe file

<br/>

Your Windows Defender might block the file. There are several issues that make this happen:

1. I do not have a digital certificate to sign the .exe file.

2. Since the file is new on the internet, it has a low reputation and its hash is unfamiliar to Windows Defender.

3. I used the PyInstaller to compile my .py file with --onefile flag, this is a red flag to Windows Defender, because the executable has to unpack all its libraries into a temp folder every time.

<br/>

- **To resolve this issue**, you might try to download packed .zip file from [Releases](https://github.com/Yehor4k/pubg/releases/). Since it has already unpacked libraries, it might help the Windows Defender not to flag the .exe file. 

- **In case this did not help you**, please, install the source code version. It requires Python and pynput library installation. [Please follow these steps.](#py-usage-aka-source-code)

> So, it just takes time before the file gets allowed and checked. I have uploaded the file to the Feedback Hub so they can review it and hopefully allow it to be used without any issues.

> The best way to use it right now is to run the source code. That is, install python, run a single cmd command "pip install pynput", and then just run the raw run.py file. But if you have the possibility to run the exe file, it would be appreciated as it would speed up the approval of the calc.exe file.

---

## 🎮 How to Use

The latest release has the new feature – Settings Window, which let's you tweak some settings.

</br>

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/4.png)

</br>

### Once the program is running, you can use the following hotkeys to measure distances:

</br>

### 1. Calibration + Measurement

**Hotkey:** `Ctrl` + `Alt` + `S`

* **Step 1**: On map hold click and drag to select a single **white grid square** (the 100x100m square) on your map to calibrate the scale.

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/1.png)

</br>

* **Step 2**: Immediately hold click and drag from **your location** to your **target's location**.

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/2.png)

</br>

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/3.png)

</br>

### 2. Measurement Only

**Hotkey:** `Alt` + `S`

* Use this if you have already calibrated and just need a new reading.
* On map simply hold click and drag from **your location** to your **target's location**.

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/2.png)

</br>

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/3.png)

---

> **Tip:** For the most accurate shots, ensure your map zoom level remains consistent after calibration, or recalibrate if you zoom in/out significantly.
