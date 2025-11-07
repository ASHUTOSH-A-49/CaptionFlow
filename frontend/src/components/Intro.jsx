// src/components/Intro.jsx
import React from "react";
import { motion } from "framer-motion";
import logo from "../assets/logo1.png";
import productImg from "../assets/logo1.png";
import FeatureIntro from "./FeatureIntro";

const Intro = () => {
// Smooth scroll handler
const handleScroll = () => {
const target = document.getElementById("translator-section");
if (target) {
target.scrollIntoView({ behavior: "smooth" });
}
};

return ( <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-950 to-indigo-900 text-indigo-100 flex flex-col">
{/* Navbar */} <nav className="flex items-center justify-between px-6 py-4 border-b border-indigo-500"> <div className="flex items-center gap-2"> <img src={logo} alt="Logo" className="h-10 w-10 object-contain" /> <h1 className="text-2xl font-bold text-indigo-400 tracking-wide">CaptionFlow </h1> </div> 
 </nav>

  {/* Main Body */}
  <div className="flex flex-col md:flex-row items-start px-8 md:px-16 py-4 gap-10 mb-8">
    {/* Left - Features / About Section */}
    <div className="w-full md:w-1/2">
      <h1 className="text-6xl font-bold text-center text-indigo-400 mb-4 pt-10">
        About Us
      </h1>
      <p className="text-lg text-gray-300 max-w-2xl mx-auto text-center mb-6 font-bold">
        CaptionFlow harnesses advanced AI to deliver instant, high-accuracy
        captions for your audio and video content. We specialize in real-time
        speech-to-text and translation, focusing particularly on multiple Indian
        languages, to make your live streams, meetings, and videos universally
        accessible. Our mission is to bridge communication gaps and ensure your
        message is understood by everyone, everywhere.
      </p>
      {/* Feature list with alternating colored divs */}
      <FeatureIntro />
    </div>

    {/* Right - Animated Image & Button */}
    <div className="w-full md:w-1/2 flex flex-col justify-center items-center mt-12 md:mt-40 gap-12">
      <motion.img
        src={productImg}
        alt="Product"
        className="w-72 md:w-96 rounded-xl shadow-lg"
        animate={{ y: [0, -20, 0] }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      <button
        onClick={handleScroll}
        className="inline-flex items-center gap-2 bg-indigo-600/30 hover:bg-indigo-600/50 text-white text-xl py-6 px-14 rounded-lg shadow-md transition-all font-bold duration-300 transform hover:-translate-y-1 hover:shadow-lg w-fit"
      >
        Get Started →
      </button>
    </div>
  </div>
</div>

);
};

export default Intro;