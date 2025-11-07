import React from "react";

export const Footer = () => {
  return (
    <footer className="w-full bg-gray-900 text-gray-400 py-6 flex flex-col items-center justify-center border-t border-gray-800">
      <p className="text-sm">© 2025 All rights reserved</p>
      <p className="text-sm mt-2 flex items-center gap-1">
        Made with <span className="text-red-500 text-lg">❤</span> by{" "}
        <span className="text-indigo-400 font-semibold">Bit_Masters</span>
      </p>
    </footer>
  );
};
