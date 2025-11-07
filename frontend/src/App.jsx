// ---------------------------VERSION - 0(not working)-------------------------
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


// -----------------WORKING VERSION 1.1 (best latency whisper fast))--------------------
import React from 'react';
import './App.css';
import Intro from './components/Intro.jsx';
import Translator from './components/Translator.jsx';
import {Footer} from './components/Footer.jsx';

// --- Placeholder Components ---
// You can move these to their own files later

// Placeholder for your main app page
const MainApp = () => (
  <div className="flex items-center justify-center h-screen bg-gray-100">
    <h1 className="text-4xl font-bold">Main App Page</h1>
  </div>
);

// Placeholder for your about page
const About = () => (
  <div className="flex items-center justify-center h-screen bg-gray-100">
    <h1 className="text-4xl font-bold">About Page</h1>
  </div>
);

// --- Main App ---
function App() {
  return (
    <>
      <Intro />
      <div id="translator-section">
        <Translator />
      </div>
      <Footer />
    </>
  );
}

export default App;

// -----------------------------------------------------------------


// ---------------------------VERSION 1.2-------------------------------------
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
//       setOriginal("");
//       setTranslated("");
//     } else {
//       socket.emit("stop_transcription");
//     }
//     setStarted(!started);
//   };

//   useEffect(() => {
//     const handleTranslatedText = (data) => {
//       setOriginal((prev) => (prev ? prev + " " : "") + data.original);
//       setTranslated((prev) => (prev ? prev + " " : "") + data.translated);
//     };
//     socket.on("translated_text", handleTranslatedText);
//     return () => {
//       socket.off("translated_text", handleTranslatedText);
//     };
//   }, []);

//   return (
//      <div style={{
//       padding: "2rem",
//       maxWidth: 900,
//       margin: "auto",
//       fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
//       backgroundColor: "#f0f2f5",
//       color: "#333",
//       minHeight: "100vh",
//       display: "flex",
//       flexDirection: "column",
//       gap: "2rem",
//       boxSizing: "border-box",
//       width: "100vw",        // Make width use full viewport width
//       height: "100vh",       // Full viewport height
//       overflowX: "hidden"    // Prevent horizontal scroll due to padding/margin
//     }}>
//       <div style={{ display: "flex", alignItems: "center", gap: "1rem", flexWrap: "wrap" }}>
//         <label htmlFor="target-lang" style={{ fontWeight: "600", fontSize: "1.1rem", whiteSpace: "nowrap" }}>
//           🎯 Select Target Language:
//         </label>
//         <select
//   id="target-lang"
//   value={langCode}
//   onChange={e => setLangCode(e.target.value)}
//   disabled={started}
//   style={{
//     padding: "0.45rem 0.75rem",
//     fontSize: "1rem",
//     borderRadius: "6px",
//     border: "1px solid #ccc",
//     minWidth: "160px"
//   }}
// >
//   <option value="bho_Deva">Bhojpuri</option>
//   <option value="hin_Deva">Hindi</option>
//   <option value="tam_Taml">Tamil</option>
//   <option value="ben_Beng">Bengali</option>
//   <option value="guj_Gujr">Gujarati</option>
//   <option value="tel_Telu">Telugu</option>
//   <option value="mar_Deva">Marathi</option>
// </select>

//         <button
//           onClick={toggle}
//           style={{
//             padding: "0.6rem 1.2rem",
//             fontSize: "1.15rem",
//             fontWeight: "600",
//             borderRadius: "6px",
//             cursor: "pointer",
//             backgroundColor: started ? "#d9534f" : "#28a745",
//             color: "#fff",
//             border: "none",
//             flexShrink: 0,
//             boxShadow: "0px 4px 8px rgba(0,0,0,0.1)",
//             transition: "background-color 0.3s ease"
//           }}
//         >
//           {started ? "🛑 Stop Listening" : "▶️ Start Listening"}
//         </button>
//       </div>

//       <div style={{
//         display: "grid",
//         gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
//         gap: "2rem"
//       }}>
//         <section style={{
//           backgroundColor: "#fff",
//           padding: "1.25rem 1.5rem",
//           borderRadius: "10px",
//           boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
//           minHeight: "180px",
//           display: "flex",
//           flexDirection: "column"
//         }}>
//           <h3 style={{
//             marginBottom: "1rem",
//             color: "#4a4a4a",
//             fontWeight: "700",
//             display: "flex",
//             alignItems: "center",
//             gap: "0.5rem"
//           }}>
//             🗣️ Recognized Speech
//           </h3>
//           <p style={{
//             whiteSpace: "pre-wrap",
//             flexGrow: 1,
//             overflowY: "auto",
//             fontSize: "1rem",
//             color: "#333",
//             lineHeight: "1.5"
//           }}>
//             {original || "Recognized text will appear here..."}
//           </p>
//         </section>

//         <section style={{
//           backgroundColor: "#fff",
//           padding: "1.25rem 1.5rem",
//           borderRadius: "10px",
//           boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
//           minHeight: "180px",
//           display: "flex",
//           flexDirection: "column"
//         }}>
//           <h3 style={{
//             marginBottom: "1rem",
//             color: "#4a4a4a",
//             fontWeight: "700",
//             display: "flex",
//             alignItems: "center",
//             gap: "0.5rem"
//           }}>
//             🌐 Translated Output
//           </h3>
//           <p style={{
//             whiteSpace: "pre-wrap",
//             flexGrow: 1,
//             overflowY: "auto",
//             fontSize: "1rem",
//             color: "#333",
//             lineHeight: "1.5"
//           }}>
//             {translated || "Translated text will appear here..."}
//           </p>
//         </section>
//       </div>
//     </div>
//   );
// }
// --------------------------------------------------------------------------------------



// --------------------------------------------VERSION 2.0(sarvam) ------------------------------
// import { useEffect, useState } from "react";
// import io from "socket.io-client";

// const socket = io("http://localhost:5000");

// export default function App() {
//   const [started, setStarted] = useState(false);
//   const [langCode, setLangCode] = useState("bho_Deva");
//   const [original, setOriginal] = useState("");
//   const [translated, setTranslated] = useState("");

//   // Start or stop transcription on button click
//   const toggle = () => {
//   if (!started) {
//     socket.emit("start_transcription", { target_lang: langCode });
//     setOriginal("");    // Clear previous captions
//     setTranslated("");
//   } else {
//     socket.emit("stop_transcription");
//   }
//   setStarted(!started);
// };


//   // Listen for backend emitted translated_text events
//   useEffect(() => {
//     const handleTranslatedText = (data) => {
//   const sourceCaption = data.source_lang_name || `[${data.source_lang}]`;
//   const targetCaption = data.target_lang_name || `[${data.target_lang}]`;
  
//   setOriginal((prev) => prev + (prev ? "\n" : "") + `${sourceCaption}: ${data.original}`);
//   setTranslated((prev) => prev + (prev ? "\n" : "") + `${targetCaption}: ${data.translated}`);
// };


//     socket.on("translated_text", handleTranslatedText);

//     // Cleanup listener on unmount
//     return () => {
//       socket.off("translated_text", handleTranslatedText);
//     };
//   }, []);

//   return (
//     <div style={{ padding: 20 }}>
//       <h1>🎤 Real-Time Speech Translator</h1>
//       <label>
//         🎯 Select Target Language:&nbsp;
//         <select value={langCode} onChange={(e) => setLangCode(e.target.value)} disabled={started}>
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
//       <button onClick={toggle}>{started ? "🛑 Stop Listening" : "▶️ Start Listening"}</button>

//       <div style={{ display: "flex", marginTop: 20, gap: 20 }}>
//         <div style={{ flex: 1 }}>
//           <h3>🗣️ Recognized Speech</h3>
//           <p style={{
//   whiteSpace: "pre-wrap",
//   minHeight: 100,
//   padding: 10,
//   border: "1px solid #ccc",
//   borderRadius: 8,
//   backgroundColor: "#272727ff",
//   overflowY: "auto",      // add this
//   maxHeight: 300          // optional max height for scroll area
// }}>
//   {original}
// </p>

//         </div>
//         <div style={{ flex: 1 }}>
//           <h3>🌐 Translated Output</h3>
//           <p style={{
//   whiteSpace: "pre-wrap",
//   minHeight: 100,
//   padding: 10,
//   border: "1px solid #ccc",
//   borderRadius: 8,
//   backgroundColor: "#272727ff",
//   overflowY: "auto",      // add this
//   maxHeight: 300          // optional max height for scroll area
// }}>
//   {translated}
// </p>

//         </div>   
//       </div>
//     </div>
//   );
// }
// ------------------------------------------------------------------


