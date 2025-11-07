import React, { useState } from "react";
import { useEffect} from "react";
import io from "socket.io-client";

const socket = io("http://localhost:5000");

const Translator = () => {
  const [targetLang, setTargetLang] = useState("hindi");

  const languages = [
  { label: "English", value: "eng_Latn" },
  { label: "Hindi", value: "hin_Deva" },
  { label: "Bengali", value: "ben_Beng" },
  { label: "Marathi", value: "mar_Deva" },
  { label: "Tamil", value: "tam_Taml" },
  { label: "Telugu", value: "tel_Telu" },
  { label: "Gujarati", value: "guj_Gujr" },
  { label: "Bhojpuri", value: "bho_Deva" },
  { label: "Sanskrit", value: "san_Deva" },
  // add others...
];



const [started, setStarted] = useState(false);
const [actualText, setActualText] = useState("");
const [translatedText, setTranslatedText] = useState("eng_Latn");
const [actualLines, setActualLines] = useState([]);
const [translatedLines, setTranslatedLines] = useState([]);


// Start transcription
const handleStart = () => {
  setActualText("");
  setTranslatedText("");
  socket.emit("start_transcription", { target_lang: targetLang });
  setStarted(true);
};
// Stop transcription
const handleStop = () => {
  socket.emit("stop_transcription");
  setStarted(false);
};

// Listen for results
useEffect(() => {
//   const handleTranslatedText = (data) => {
//     setActualText(prev => prev + (prev ? "\n" : "") + data.original);
//     setTranslatedText(prev => prev + (prev ? "\n" : "") + data.translated);
//   };

//   socket.on("translated_text", handleTranslatedText);

//   return () => {
//     socket.off("translated_text", handleTranslatedText);
//   };
const handleTranslatedText = (data) => {
    setActualLines(prev => {
      const updated = [...prev, data.original];
      return updated.length > 2 ? updated.slice(-2) : updated;
    });
    setTranslatedLines(prev => {
      const updated = [...prev, data.translated];
      return updated.length > 2 ? updated.slice(-2) : updated;
    });
  };

  socket.on("translated_text", handleTranslatedText);
  return () => {
    socket.off("translated_text", handleTranslatedText);
  };
}, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-950 to-indigo-900 px-4">
      <div className="w-full max-w-5xl bg-gray-800 rounded-2xl shadow-xl border border-gray-700 p-8 space-y-8 flex flex-col">
        {/* Title */}
        <h1 className="text-3xl sm:text-4xl font-bold text-center text-indigo-100 tracking-tight">
          Real-Time Captioning
        </h1>

        {/* Target Language Dropdown (Full width, outside the text columns) */}
        <div className="w-full">
          <label className="block text-xs uppercase font-semibold text-gray-400 mb-2">
            Target Language
          </label>
          <select
            value={targetLang} onChange={e => setTargetLang(e.target.value)}
            className="w-full bg-gray-700 text-gray-200 border border-gray-600 rounded-lg px-4 py-2 mb-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition pr-2"
          >
            {languages.map(lang => (
    <option key={lang.value} value={lang.value}>
      {lang.label}
    </option>
            ))}
          </select>
        </div>

        {/* Language & Text Sections */}
        <div className="flex flex-col md:flex-row gap-6 md:gap-12 items-center md:items-stretch justify-center transition-all">
          
          {/* Actual Text */}
          <div className="flex flex-col w-full md:w-1/2 bg-gray-900 rounded-xl p-5 shadow transition-all">
            <label className="block text-sm text-gray-500 mb-2 font-medium">
              Actual Text
            </label>
            {/* className="w-full h-32 bg-gray-800 border border-gray-700 rounded-lg p-3 text-gray-100 focus:outline-none focus:border-indigo-600 resize-none transition" */}
            <div className="w-full h-32 bg-gray-800 border border-gray-700 rounded-lg p-3 text-gray-100 font-semibold text-lg focus:outline-none focus:border-indigo-600 resize-none transition"
>
  {actualLines.map((line, idx) => (
    <div key={idx} >{line}</div>
  ))}
</div>

          </div>

          {/* Translated Text */}
          <div className="flex flex-col w-full md:w-1/2 bg-gray-900 rounded-xl p-5 shadow transition-all">
            <label className="block text-sm text-gray-500 mb-2 font-medium">
              Translated Text
            </label>
            <div className="w-full h-32 bg-gray-800 border border-gray-700 rounded-lg p-3 text-gray-100 font-semibold text-lg focus:outline-none focus:border-indigo-600 resize-none transition"
>
  {translatedLines.map((line, idx) => (
    <div key={idx} className="caption-line">{line}</div>
  ))}
</div>

          </div>
        </div>

        {/* Start button */}
        {/* className="w-full md:w-auto self-center bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 px-8 rounded-xl shadow-md transition transform hover:scale-[1.03] active:scale-95 duration-150 text-lg" */}
        {!started ? (
  <button onClick={handleStart} className="w-full md:w-auto self-center bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 px-8 rounded-xl shadow-md transition transform hover:scale-[1.03] active:scale-95 duration-150 text-lg">Start Generation!</button>
) : (
  <button onClick={handleStop} className="w-full md:w-auto self-center bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 px-8 rounded-xl shadow-md transition transform hover:scale-[1.03] active:scale-95 duration-150 text-lg">Stop Listening</button>
)}

      </div>
    </div>
  );
};

export default Translator;