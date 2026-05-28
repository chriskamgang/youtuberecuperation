import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys

try:
    import yt_dlp
except ImportError:
    messagebox.showerror(
        "Dependance manquante",
        "yt-dlp n'est pas installe.\n\nExecute cette commande dans le terminal :\n\npip install yt-dlp"
    )
    sys.exit(1)


class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Telecharger Videos YouTube")
        self.root.geometry("720x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#1B2A4A")

        self.download_folder = os.path.expanduser("~/Downloads")
        self.is_downloading = False
        self._stop_event = threading.Event()
        self._current_ydl = None

        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self.root, text="Telecharger Videos YouTube",
            font=("Arial", 18, "bold"), fg="#F5A623", bg="#1B2A4A"
        ).pack(pady=(20, 5))

        tk.Label(
            self.root, text="Colle les liens YouTube (videos ou playlistes, un par ligne)",
            font=("Arial", 11), fg="#AABBD0", bg="#1B2A4A"
        ).pack()

        # Zone de texte
        frame_links = tk.Frame(self.root, bg="#1B2A4A")
        frame_links.pack(padx=20, pady=10, fill="both")

        self.txt_links = tk.Text(
            frame_links, height=10, font=("Courier", 11),
            bg="#0D1B2E", fg="#FFFFFF", insertbackground="white",
            relief="flat", bd=0, padx=8, pady=8, wrap="word"
        )
        self.txt_links.pack(fill="both", expand=True)
        self.txt_links.insert("1.0", "https://www.youtube.com/watch?v=...\nhttps://www.youtube.com/watch?v=...")
        scrollbar = tk.Scrollbar(frame_links, command=self.txt_links.yview)
        self.txt_links.configure(yscrollcommand=scrollbar.set)

        # Format
        frame_opts = tk.Frame(self.root, bg="#1B2A4A")
        frame_opts.pack(padx=20, pady=5, fill="x")

        tk.Label(frame_opts, text="Format :", fg="#AABBD0", bg="#1B2A4A", font=("Arial", 11)).pack(side="left")
        self.format_var = tk.StringVar(value="mp4_best")
        formats = [
            ("Video MP4 (meilleure qualite)", "mp4_best"),
            ("Video MP4 1080p", "mp4_1080"),
            ("Video MP4 720p", "mp4_720"),
            ("Audio MP3 seulement", "mp3"),
        ]
        self.format_combo = ttk.Combobox(
            frame_opts, textvariable=self.format_var, state="readonly",
            width=30, font=("Arial", 10)
        )
        self.format_combo["values"] = [f[0] for f in formats]
        self.format_combo.current(0)
        self.format_combo.pack(side="left", padx=(8, 0))
        self._format_map = {f[0]: f[1] for f in formats}

        # Dossier
        frame_dest = tk.Frame(self.root, bg="#1B2A4A")
        frame_dest.pack(padx=20, pady=8, fill="x")

        tk.Label(frame_dest, text="Dossier :", fg="#AABBD0", bg="#1B2A4A", font=("Arial", 11)).pack(side="left")
        self.lbl_folder = tk.Label(
            frame_dest, text=self.download_folder,
            fg="#FFFFFF", bg="#0D1B2E", font=("Arial", 10),
            anchor="w", padx=6, width=50
        )
        self.lbl_folder.pack(side="left", padx=(8, 6))
        tk.Button(
            frame_dest, text="Choisir", command=self._choose_folder,
            bg="#F5A623", fg="#1B2A4A", font=("Arial", 10, "bold"),
            relief="flat", padx=10, cursor="hand2"
        ).pack(side="left")

        # Barre de progression
        self.progress = ttk.Progressbar(self.root, mode="indeterminate", length=680)
        self.progress.pack(padx=20, pady=(10, 0))

        # Log
        frame_log = tk.Frame(self.root, bg="#1B2A4A")
        frame_log.pack(padx=20, pady=8, fill="both", expand=True)

        self.txt_log = tk.Text(
            frame_log, height=6, font=("Courier", 10),
            bg="#0A1520", fg="#5EE56E", insertbackground="green",
            relief="flat", bd=0, padx=8, pady=6, state="disabled"
        )
        self.txt_log.pack(fill="both", expand=True)

        # Boutons
        frame_btns = tk.Frame(self.root, bg="#1B2A4A")
        frame_btns.pack(pady=10)

        self.btn_download = tk.Button(
            frame_btns, text="  TELECHARGER  ",
            command=self._start_download,
            bg="#F5A623", fg="#1B2A4A", font=("Arial", 13, "bold"),
            relief="flat", padx=20, pady=8, cursor="hand2"
        )
        self.btn_download.pack(side="left", padx=8)

        self.btn_stop = tk.Button(
            frame_btns, text="  STOP  ",
            command=self._stop_download,
            bg="#C0392B", fg="#FFFFFF", font=("Arial", 13, "bold"),
            relief="flat", padx=20, pady=8, cursor="hand2",
            state="disabled"
        )
        self.btn_stop.pack(side="left", padx=8)

        tk.Button(
            frame_btns, text="Effacer",
            command=self._clear,
            bg="#2E4070", fg="#FFFFFF", font=("Arial", 11),
            relief="flat", padx=16, pady=8, cursor="hand2"
        ).pack(side="left", padx=8)

    def _choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.lbl_folder.config(text=folder)

    def _log(self, message):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", message + "\n")
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    def _clear(self):
        self.txt_links.delete("1.0", "end")
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.config(state="disabled")

    def _stop_download(self):
        if self.is_downloading:
            self._stop_event.set()
            self._log("\n  Arret demande... fin de la video en cours.")
            self.btn_stop.config(state="disabled", text="Arret...")

    def _has_ffmpeg(self):
        import shutil
        return shutil.which("ffmpeg") is not None

    def _get_ydl_opts(self, fmt_key):
        out_template = os.path.join(self.download_folder, "%(title)s.%(ext)s")
        ffmpeg = self._has_ffmpeg()

        if fmt_key == "mp3":
            if not ffmpeg:
                return {
                    "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio",
                    "outtmpl": out_template,
                    "quiet": True,
                    "progress_hooks": [self._progress_hook],
                }
            return {
                "format": "bestaudio/best",
                "outtmpl": out_template,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "quiet": True,
                "progress_hooks": [self._progress_hook],
            }

        if not ffmpeg:
            if fmt_key == "mp4_720":
                fmt = "best[height<=720][ext=mp4]/best[height<=720]/best[ext=mp4]/best"
            elif fmt_key == "mp4_1080":
                fmt = "best[height<=1080][ext=mp4]/best[height<=1080]/best[ext=mp4]/best"
            else:
                fmt = "best[ext=mp4]/best"
        else:
            if fmt_key == "mp4_1080":
                fmt = "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best"
            elif fmt_key == "mp4_720":
                fmt = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best"
            else:
                fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

        opts = {
            "format": fmt,
            "outtmpl": out_template,
            "quiet": True,
            "progress_hooks": [self._progress_hook],
            "retries": 15,
            "fragment_retries": 15,
            "socket_timeout": 30,
            "http_chunk_size": 1048576,
            "ignoreerrors": True,   # continue si une video de la playlist echoue
            "continuedl": True,     # reprend les telechargements interrompus
            "nooverwrites": True,   # ne re-telecharge pas les videos deja presentes
        }
        if ffmpeg:
            opts["merge_output_format"] = "mp4"
        return opts

    def _progress_hook(self, d):
        if self._stop_event.is_set():
            raise yt_dlp.utils.DownloadCancelled()
        if d["status"] == "downloading":
            filename = os.path.basename(d.get("filename", ""))
            percent = d.get("_percent_str", "").strip()
            speed = d.get("_speed_str", "").strip()
            playlist_index = d.get("info_dict", {}).get("playlist_index")
            playlist_count = d.get("info_dict", {}).get("n_entries")
            prefix = f"[{playlist_index}/{playlist_count}] " if playlist_index else ""
            self.root.after(0, self._log, f"  {prefix}{filename[:45]}... {percent} ({speed})")
        elif d["status"] == "finished":
            self.root.after(0, self._log, f"  Termine : {os.path.basename(d['filename'])}")

    def _start_download(self):
        if self.is_downloading:
            return

        raw = self.txt_links.get("1.0", "end").strip()
        links = [l.strip() for l in raw.splitlines() if l.strip().startswith("http")]

        if not links:
            messagebox.showwarning("Aucun lien", "Colle au moins un lien YouTube valide.")
            return

        fmt_label = self.format_var.get()
        fmt_key = self._format_map[fmt_label]

        self._stop_event.clear()
        self.is_downloading = True
        self.btn_download.config(state="disabled", text="Telechargement...")
        self.btn_stop.config(state="normal", text="  STOP  ")
        self.progress.start(10)
        self._log(f"Debut du telechargement de {len(links)} lien(s)...")
        self._log(f"Format : {fmt_label}")
        self._log(f"Dossier : {self.download_folder}")
        self._log("-" * 60)

        thread = threading.Thread(target=self._download_all, args=(links, fmt_key), daemon=True)
        thread.start()

    def _download_all(self, links, fmt_key):
        success = 0
        errors = 0

        for i, url in enumerate(links, 1):
            if self._stop_event.is_set():
                self.root.after(0, self._log, "\n  Telechargement arrete par l'utilisateur.")
                break

            is_playlist = "playlist" in url or "list=" in url
            type_label = "PLAYLIST" if is_playlist else "VIDEO"
            self.root.after(0, self._log, f"\n[{i}/{len(links)}] [{type_label}] {url}")
            if is_playlist:
                self.root.after(0, self._log, "  Lecture de la playlist en cours...")

            downloaded_files = []

            def hook(d, _files=downloaded_files):
                if d["status"] == "finished":
                    _files.append(d.get("filename", ""))
                self._progress_hook(d)

            opts = self._get_ydl_opts(fmt_key)
            if is_playlist:
                opts["outtmpl"] = os.path.join(
                    self.download_folder,
                    "%(playlist_title)s",
                    "%(playlist_index)02d - %(title)s.%(ext)s"
                )
            opts["progress_hooks"] = [hook]

            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    self._current_ydl = ydl
                    ret = ydl.download([url])
                self._current_ydl = None
                if ret == 0 or downloaded_files:
                    success += 1
                else:
                    errors += 1
            except yt_dlp.utils.DownloadCancelled:
                self.root.after(0, self._log, "  Arrete.")
                break
            except Exception as e:
                self._current_ydl = None
                err_msg = str(e)[:120]
                if downloaded_files:
                    self.root.after(0, self._log, f"  Avertissement : {err_msg}")
                    success += 1
                else:
                    self.root.after(0, self._log, f"  ERREUR : {err_msg}")
                    errors += 1

        self.root.after(0, self._download_done, success, errors)

    def _download_done(self, success, errors):
        self.progress.stop()
        self.is_downloading = False
        self._current_ydl = None
        self.btn_download.config(state="normal", text="  TELECHARGER  ")
        self.btn_stop.config(state="disabled", text="  STOP  ")
        self._log("\n" + "=" * 60)
        self._log(f"TERMINE : {success} succes, {errors} erreur(s)")
        self._log(f"Dossier : {self.download_folder}")

        if not self._stop_event.is_set():
            if errors == 0:
                messagebox.showinfo("Termine !", f"{success} video(s) telechargee(s) avec succes !")
            else:
                messagebox.showwarning("Termine avec erreurs", f"{success} succes, {errors} echec(s).\nVoir le log pour les details.")


def main():
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()


if __name__ == "__main__":
    if "--test" in sys.argv:
        import tkinter as tk
        import yt_dlp
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        print("TEST OK : imports et tkinter fonctionnels")
        sys.exit(0)
    main()
