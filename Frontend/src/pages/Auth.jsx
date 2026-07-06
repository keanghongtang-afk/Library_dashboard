import { useState } from "react";
function Auth() {
    let welcome_msg,welcome_head, banner_class;
    const [auth_type, setAuthType] = useState(true);
    if(auth_type){
        banner_class = "login";
        welcome_head = "Welcome Back!";
        welcome_msg = "Log in to manage your borrowed books, reservations, and reading history.";
    }else{
        banner_class = "signup";
        welcome_head = "Welcome, Book Lover!";
        welcome_msg = "Create an account to borrow books, save your favorites, and discover new reads.";
    }

    return (
        <div className="auth-interface
         border border-2 rounded rounded-3
          d-flex justify-content-center align-items-center flex-wrap
          p-3
          ">
            <div className="Login-container
            d-flex justify-content-center align-items-center ">
                <div className="auth-header">
                    <h2>Login</h2>
                </div>
                <div className="auth-body
                d-flex justify-content-center align-items-center">
                    <input type="email" placeholder="Email" />
                    <input type="password" placeholder="Password" />
                    <button type="submit">Login</button>
                    <div className="auth-footer">
                        <p>Don't have an account? <a href="#signup" onClick={() => {setAuthType(false)}}>Register</a></p>
                    </div>
                </div>
            </div>
            <div className="Singup-container
            d-flex justify-content-center align-items-center">
                <div className="auth-header">
                    <h2>SignUp</h2>
                </div>
                <div className="auth-body
                d-flex justify-content-center align-items-center">
                    <input type="text" placeholder="Name"/>
                    <input type="email" placeholder="Email" />
                    <input type="password" placeholder="Password" />
                    <input type="password" placeholder="Confirm Password"/>
                    <button type="submit">SignUp</button>
                    <div className="auth-footer">
                        <p>Already have an account? <a href="#login" onClick={() => {setAuthType(true)}}>Login</a></p>
                    </div>
                </div>
            </div>
            <div className={`${banner_class} d-flex justify-content-center align-items-center`}>
                <h2>{welcome_head}</h2>
                <p>{welcome_msg}</p>
            </div>
        </div>
    );
}

export default Auth;