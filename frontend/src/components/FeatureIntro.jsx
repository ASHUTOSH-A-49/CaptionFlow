import React from "react";

const features = [
  "Real-time caption generation from audio or video",
  "Translate captions into multiple Indian languages",
  "Accurate speech recognition powered by AI",
  "Seamless integration with live video streams",
];

const FeatureIntro = () => {
  return (
    // REMOVED 'min-h-screen' to fix extra padding
    <div className="text-white flex flex-col items-start pt-5 space-y-4">
      {/* Centered the heading */}
      <h2 className="text-4xl font-bold text-indigo-400 mb-6 text-center w-full">
        Key Features
      </h2>

      {features.map((feature, index) => {
        const isLeft = index % 2 === 0;
        return (
          // Kept the padding to push boxes inward
          <div
            key={index}
            className={`flex w-full ${
              isLeft ? "justify-start pl-16" : "justify-end pr-16"
            }`}
          >
            <div className="bg-indigo-600/30 backdrop-blur-sm p-6 rounded-lg shadow-lg max-w-md text-gray-100 font-semibold">
              {feature}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default FeatureIntro;