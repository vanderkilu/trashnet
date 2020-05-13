import React from "react";
import { Text, View, TouchableOpacity, StyleSheet } from "react-native";
import { NavigationProp } from "@react-navigation/native";

type ParamList = {
  Dashboard: undefined;
  Screen: undefined;
  CameraView: undefined;
};

type SplashScreenProps = {
  navigation: NavigationProp<ParamList, "Screen">;
};

const SplashScreen: React.FC<SplashScreenProps> = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.headerText}>TRASHNET</Text>
      <TouchableOpacity style={styles.button}>
        <Text
          style={{ textAlign: "center", color: "#ffffff" }}
          onPress={() => navigation.navigate("Dashboard")}
        >
          Tap to begin
        </Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center"
  },
  headerText: {
    fontSize: 30,
    fontWeight: "bold",
    justifyContent: "center"
  },
  button: {
    width: 150,
    padding: 10,
    borderRadius: 5,
    marginTop: 50,
    shadowOpacity: 0.2,
    backgroundColor: "#41ded2"
  }
});

export default SplashScreen;
