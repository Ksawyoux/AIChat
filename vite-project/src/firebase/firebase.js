// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore, collection, addDoc } from 'firebase/firestore';
import {getAuth} from "firebase/auth";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "firebase_apiKey",
  authDomain: "firebase_authDomain",
  projectId: "firebase_projectId",
  storageBucket: "firebase_storageBucket",
  messagingSenderId: "firebase_messagingSenderId",
  appId: "firebase_appId",
  measurementId: "G-58HL6RCDNG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app); 

export { db, collection, addDoc, app };
