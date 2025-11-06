// import { useEffect, useState } from "react";
// import io from "socket.io-client";

// const socket = io("http://localhost:5000");

// export default function App() {
//   const [started, setStarted] = useState(false);
//   const [langCode, setLangCode] = useState("bho_Deva");
//   const [original, setOriginal] = useState("");
//   const [translated, setTranslated] = useState("");

//   const toggle = () => {
//     if (!started) {
//       socket.emit("start_transcription", { target_lang: langCode });
//     } else {
//       socket.emit("stop_transcription");
//     }
//     setStarted(!started);
//   };

//   useEffect(() => {
//     socket.on("translated_text", (data) => {
//       setOriginal((prev) => prev + " " + data.original);
//       setTranslated((prev) => prev + " " + data.translated);
//     });
//     return () => socket.off("translated_text");
//   }, []);

//   return (
//     <div style={{ padding: 20 }}>
//       <h1>🎤 Real-Time Speech Translator</h1>
//       <label>
//         🎯 Select Target Language:&nbsp;
//         <select value={langCode} onChange={(e) => setLangCode(e.target.value)}>
//           <option value="bho_Deva">Bhojpuri</option>
//           <option value="hin_Deva">Hindi</option>
//           <option value="tam_Taml">Tamil</option>
//           <option value="ben_Beng">Bengali</option>
//           <option value="guj_Gujr">Gujarati</option>
//           <option value="tel_Telu">Telugu</option>
//           <option value="mar_Deva">Marathi</option>
//         </select>
//       </label>

//       <br /><br />
//       <button onClick={toggle}>
//         {started ? "🛑 Stop Listening" : "▶️ Start Listening"}
//       </button>

//       <div style={{ display: "flex", marginTop: 20, gap: 20 }}>
//         <div style={{ flex: 1 }}>
//           <h3>🗣️ Recognized Speech</h3>
//           <p>{original}</p>
//         </div>
//         <div style={{ flex: 1 }}>
//           <h3>🌐 Translated Output</h3>
//           <p>{translated}</p>
//         </div>
//       </div>
//     </div>
//   );
// }

import { useEffect, useState } from "react";
import io from "socket.io-client";

const socket = io("http://localhost:5000");

export default function App() {
  const [started, setStarted] = useState(false);
  const [langCode, setLangCode] = useState("bho_Deva");
  const [original, setOriginal] = useState("");
  const [translated, setTranslated] = useState("");

  // Start or stop transcription on button click
  const toggle = () => {
    if (!started) {
      socket.emit("start_transcription", { target_lang: langCode });
    } else {
      socket.emit("stop_transcription");
    }
    setStarted(!started);
  };

  // Listen for backend emitted translated_text events
  useEffect(() => {
    const handleTranslatedText = (data) => {
      setOriginal((prev) => prev + (prev ? " " : "") + data.original);
      setTranslated((prev) => prev + (prev ? " " : "") + data.translated);
    };

    socket.on("translated_text", handleTranslatedText);

    // Cleanup listener on unmount
    return () => {
      socket.off("translated_text", handleTranslatedText);
    };
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>🎤 Real-Time Speech Translator</h1>
      <label>
        🎯 Select Target Language:&nbsp;
        <select value={langCode} onChange={(e) => setLangCode(e.target.value)} disabled={started}>
          <option value="bho_Deva">Bhojpuri</option>
          <option value="hin_Deva">Hindi</option>
          <option value="tam_Taml">Tamil</option>
          <option value="ben_Beng">Bengali</option>
          <option value="guj_Gujr">Gujarati</option>
          <option value="tel_Telu">Telugu</option>
          <option value="mar_Deva">Marathi</option>
        </select>
      </label>

      <br /><br />
      <button onClick={toggle}>{started ? "🛑 Stop Listening" : "▶️ Start Listening"}</button>

      <div style={{ display: "flex", marginTop: 20, gap: 20 }}>
        <div style={{ flex: 1 }}>
          <h3>🗣️ Recognized Speech</h3>
          <p style={{ whiteSpace: "pre-wrap", minHeight: 100, padding: 10, border: "1px solid #ccc", borderRadius: 8, backgroundColor: "#f9f9f9" }}>
            {original}
          </p>
        </div>
        <div style={{ flex: 1 }}>
          <h3>🌐 Translated Output</h3>
          <p style={{ whiteSpace: "pre-wrap", minHeight: 100, padding: 10, border: "1px solid #ccc", borderRadius: 8, backgroundColor: "#f9f9f9" }}>
            {translated}
          </p>
        </div>   
      </div>
    </div>
  );
}

