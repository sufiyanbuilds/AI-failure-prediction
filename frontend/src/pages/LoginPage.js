import { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import "../styles/LoginPage.css";

export default function LoginPage() {

  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  
  const handleLogin = () => {

    if (username === "admin" && password === "admin123") {

      localStorage.setItem("admin", "true");

      navigate("/department");

    } else {

      alert("Invalid Username or Password");

    }
  };

  return (

    <div className="login-container">

      <div className="login-card">

        <h1 className="login-title">
          Department Login
        </h1>

        <input
          className="login-input"
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <div className="password-wrapper">
          <input
            className="login-input"
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <span
            className="password-toggle"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? <FaEyeSlash /> : <FaEye />}
          </span>
        </div>

        <button
          className="login-btn"
          onClick={handleLogin}
        >
          Login
        </button>

      </div>

    </div>
  );
}