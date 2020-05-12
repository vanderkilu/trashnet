import React from "react";
import { Text, View, TouchableOpacity, Image } from "react-native";

const SplashScreen: React.FC<{}> = () => {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      <Text
        style={{
          fontSize: 30,
          fontWeight: "bold",
          justifyContent: "center"
        }}
      >
        TRASHNET
      </Text>
      <TouchableOpacity
        style={{
          width: 150,
          padding: 10,
          borderRadius: 5,
          marginTop: 50,
          shadowOpacity: 0.2,
          backgroundColor: "#41ded2"
        }}
      >
        <Text style={{ textAlign: "center", color: "#ffffff" }}>
          Tap to begin
        </Text>
      </TouchableOpacity>
    </View>
  );
};

export default SplashScreen;
