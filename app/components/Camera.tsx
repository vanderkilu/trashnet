import React, { useState, useEffect } from "react";
import { View, Text, TouchableOpacity } from "react-native";
import { Camera } from "expo-camera";
import * as Permissions from "expo-permissions";

const CameraView: React.FC<{}> = () => {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const type = Camera.Constants.Type.back;
  useEffect(() => {
    (async () => {
      const { status } = await Permissions.askAsync(Permissions.CAMERA);
      setHasPermission(status === "granted");
    })();
  }, []);

  if (hasPermission === null) return <View />;
  if (hasPermission === false)
    return (
      <View>
        <Text>No Access Granted To Camera</Text>
      </View>
    );
  return (
    <View style={{ flex: 1 }}>
      <Camera
        style={{ flex: 1, flexDirection: "row", justifyContent: "center" }}
        type={type}
      >
        <View style={{ alignSelf: "flex-end" }}>
          <TouchableOpacity style={{ alignSelf: "center" }}>
            <View
              style={{
                borderWidth: 5,
                borderRadius: 100 / 2,
                borderColor: "grey",
                height: 100,
                width: 100,
                display: "flex",
                backgroundColor: "#ffffff",
                justifyContent: "center",
                alignItems: "center"
              }}
            />
          </TouchableOpacity>
        </View>
      </Camera>
    </View>
  );
};
export default CameraView;
