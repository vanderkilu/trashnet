import React from "react";
import { View, Text, StyleSheet, Image, TouchableOpacity } from "react-native";
import { NavigationProp } from "@react-navigation/native";

type ParamList = {
  Dashboard: undefined;
  Screen: undefined;
  CameraView: undefined;
};

type DashboardProp = {
  navigation: NavigationProp<ParamList, "Dashboard">;
};

const Dashboard: React.FC<DashboardProp> = ({ navigation }) => {
  const items = [
    { name: "cardboard", count: 10, backgroundColor: "#a2edff" },
    { name: "metal", count: 20, backgroundColor: "#ECA3D0" },
    { name: "plastic", count: 30, backgroundColor: "#FFC387" },
    { name: "glass", count: 40, backgroundColor: "#97B7FE" },
    { name: "paper", count: 30, backgroundColor: "#41E1CB" },
    { name: "trash", count: 60, backgroundColor: "#FEA499" }
  ];
  return (
    <View style={styles.container}>
      {items.map((item, i) => (
        <View
          style={{
            ...styles.item,
            ...{ backgroundColor: item.backgroundColor }
          }}
          key={i}
        >
          <View>
            <Text style={styles.mainText}>{item.name}</Text>
            <Text style={styles.subText}>{item.count}</Text>
          </View>
        </View>
      ))}
      <TouchableOpacity
        style={styles.cameraContainer}
        onPress={() => navigation.navigate("CameraView")}
      >
        <Image source={require("../assets/camera.png")} style={styles.image} />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "row",
    flexWrap: "wrap",
    marginTop: 80,
    justifyContent: "center",
    alignItems: "center",
    padding: 20
  },
  mainText: {
    fontSize: 16,
    color: "#ffffff",
    textTransform: "uppercase"
  },
  subText: {
    fontSize: 14,
    textAlign: "center",
    color: "#ffffff",
    fontWeight: "bold"
  },
  item: {
    flexBasis: "30%",
    backgroundColor: "#a2edff",
    height: 120,
    borderRadius: 10,
    padding: 5,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 10,
    marginRight: 5
  },
  cameraContainer: {
    width: 100,
    height: 100,
    borderStyle: "solid",
    borderColor: "#e0e0e0",
    borderWidth: 2,
    borderRadius: 200 / 2,
    marginTop: 100,
    justifyContent: "center",
    alignItems: "center"
  },
  image: {
    width: 60,
    height: 60
  }
});

export default Dashboard;
