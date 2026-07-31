import { useState } from "react";
import { detectLanguage } from "./api";
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Languages, Loader2, CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

// Supported languages list
const SUPPORTED_LANGUAGES = [
  "English", "Hindi", "Urdu", "Arabic", "Spanish",
  "Tamil", "Korean", "Persian", "Pushto", "Portuguese",
  "Indonesian", "Romanian", "Thai", "Dutch", "Latin"
];

const LanguageIdentifier = () => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showLangList, setShowLangList] = useState(false);

  // Identify Language (Backend Call)
  const handleIdentify = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const lang = await detectLanguage(text); // REAL BACKEND CALL

      setResult({
        language: lang,
        confidence: 98.5 // until backend support confidence
      });

    } catch (err) {
      setError("Failed to identify language.");
    }

    setLoading(false);
  };

  // =====================  UI STYLES  =====================
  const styles = {
    container: {
      minHeight: '100vh',
      width: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%)',
      fontFamily: '"Segoe UI", sans-serif',
      padding: '20px',
    },
    card: {
      width: '100%',
      maxWidth: '550px',
      background: 'rgba(255, 255, 255, 0.15)',
      backdropFilter: 'blur(20px)',
      borderRadius: '24px',
      border: '1px solid rgba(255, 255, 255, 0.3)',
      padding: '40px',
      color: 'white',
      position: 'relative'
    },
    title: {
      textAlign: 'center',
      fontSize: '32px',
      fontWeight: '800'
    },
    textarea: {
      width: '100%',
      height: '150px',
      background: 'rgba(0, 0, 0, 0.2)',
      border: '2px solid rgba(255, 255, 255, 0.1)',
      borderRadius: '16px',
      padding: '15px',
      color: 'white',
      fontSize: '16px',
      marginBottom: '20px',
      resize: 'none'
    },
    button: {
      width: '100%',
      padding: '16px',
      border: 'none',
      borderRadius: '12px',
      background: text ? 'white' : 'rgba(255,255,255,0.3)',
      color: text ? '#C850C0' : 'rgba(255,255,255,0.5)',
      fontSize: '18px',
      cursor: text ? 'pointer' : 'not-allowed',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '10px'
    },
    resultBox: {
      marginTop: '30px',
      background: 'rgba(0, 255, 127, 0.2)',
      border: '1px solid rgba(0, 255, 127, 0.4)',
      padding: '20px',
      borderRadius: '16px',
      display: 'flex',
      justifyContent: 'space-between'
    },
    modalOverlay: {
      position: 'absolute',
      top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.6)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: '24px',
      zIndex: 10
    },
    modalContent: {
      background: 'rgba(30,30,30,0.95)',
      padding: '20px',
      width: '90%',
      borderRadius: '16px',
      color: 'white'
    },
    langGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(2, 1fr)',
      gap: '10px'
    }
  };

  // ========================================================

  return (
    <div style={styles.container}>
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        style={styles.card}
      >

        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "20px" }}>
          <div style={{ ...styles.iconWrapper }}>
            <Languages size={32} color="white" />
          </div>

          <h1 style={styles.title}>Language Detector</h1>
          <p>Paste text to identify its origin</p>

          <button
            onClick={() => setShowLangList(true)}
            style={{
              background: "transparent",
              border: "1px solid white",
              padding: "6px 12px",
              borderRadius: "20px",
              color: "white",
              cursor: "pointer"
            }}>
            <Info size={14} /> View supported languages
          </button>
        </div>

        {/* Textbox */}
        <textarea
          style={styles.textarea}
          placeholder="Type some text..."
          value={text}
          onChange={(e) => {
            const input = e.target.value;
            setText(input);

            // ⭐ Hide result ONLY when input is fully cleared
            if (input.trim().length === 0) {
              setResult(null);
            }
          }}
        />

        {/* Button */}
        <motion.button
          whileHover={text ? { scale: 1.02 } : {}}
          whileTap={text ? { scale: 0.98 } : {}}
          style={styles.button}
          disabled={!text || loading}
          onClick={handleIdentify}
        >
          {loading ? <Loader2 className="animate-spin" /> : <Sparkles />}
          {loading ? "Analyzing..." : "Identify Language"}
        </motion.button>

        {/* RESULT */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              style={styles.resultBox}
            >
              <div style={{ display: 'flex', gap: '15px' }}>
                <CheckCircle2 size={30} color="lightgreen" />
                <div>
                  <small style={{ opacity: 0.8 }}>Detected</small>
                  <h2 style={{ margin: 0 }}>{result.language}</h2>
                </div>
              </div>

              <div style={{ textAlign: "right" }}>
                <small style={{ opacity: 0.8 }}>Confidence</small>
                <h3 style={{ margin: 0 }}>{result.confidence}%</h3>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* ERROR */}
        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{
              ...styles.resultBox,
              background: 'rgba(255,0,0,0.2)',
              borderColor: 'rgba(255,0,0,0.4)'
            }}
          >
            <AlertCircle size={20} color="red" />
            <span>{error}</span>
          </motion.div>
        )}

        {/* Supported Languages Modal */}
        <AnimatePresence>
          {showLangList && (
            <motion.div
              style={styles.modalOverlay}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <motion.div
                style={styles.modalContent}
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0.8 }}
              >
                <button
                  onClick={() => setShowLangList(false)}
                  style={{
                    position: 'absolute',
                    right: '20px',
                    top: '20px',
                    background: 'none',
                    border: 'none',
                    color: 'white'
                  }}
                >
                  <X size={20} />
                </button>

                <h3>Supported Languages</h3>
                <div style={styles.langGrid}>
                  {SUPPORTED_LANGUAGES.map((lang, i) => (
                    <div key={i} style={{
                      padding: "8px",
                      background: "rgba(255,255,255,0.1)",
                      textAlign: "center",
                      borderRadius: "8px"
                    }}>
                      {lang}
                    </div>
                  ))}
                </div>

              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

      </motion.div>
    </div>
  );
};

export default LanguageIdentifier;
