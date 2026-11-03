import React, { useState, useEffect, createContext } from "react";
import { setToken, getToken, removeToken } from "../api/token";
import { useUser } from "../hooks/useUser";

export const AuthContext = createContext({
  auth: undefined,
  login: () => null,
  logout: () => null,
});

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(undefined);
  const { getMe } = useUser();

  useEffect(() => {
    (async () => {
      const token = getToken();
      if (!token) {
        setAuth(null);
      } else {
        try {
          const me = await getMe(token);
          setAuth({ token, me });
        } catch (error) {
          console.error("Error al reanudar sesión:", error);
          logout();
        }
      }
    })();
  }, []);

  const login = async (token) => {
    setToken(token);
    try {
      const me = await getMe(token);
      setAuth({ token, me });
    } catch (error) {
      console.error(error);
      logout();
    }
  };

  const logout = () => {
    setAuth(null);
    removeToken();
  };

  const valueContext = {
    auth,
    login,
    logout,
  };

  if (auth === undefined) return null;

  return (
    <AuthContext.Provider value={valueContext}>{children}</AuthContext.Provider>
  );
}
