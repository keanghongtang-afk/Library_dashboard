import Login from "./pages/Login";
import { useState, useEffect } from "react";
export default function App() {
  const [islogin, setislogin] = useState(islogin === localStorage.getItem("islogin"));
  useEffect(() => {
    setislogin(islogin === localStorage.getItem("islogin"));
  },[islogin])
  if(!islogin){
    return <Login />
  }
  return (
    <div>
    </div>
  );
}