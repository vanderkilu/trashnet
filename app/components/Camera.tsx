import React, { useState, useEffect } from "react";
import { View, Text, TouchableOpacity, Image } from "react-native";
import { Camera } from "expo-camera";
import * as Permissions from "expo-permissions";
import APIService from "../api";

const CameraView: React.FC<{}> = () => {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [cameraRef, setCameraRef] = useState<Camera | null>(null);
  const [photo, setPhoto] = useState();
  const [isCameraMode, setIsCameraMode] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const type = Camera.Constants.Type.back;
  useEffect(() => {
    (async () => {
      const { status } = await Permissions.askAsync(Permissions.CAMERA);
      setHasPermission(status === "granted");
    })();
  }, []);

  const takeShot = async () => {
    if (cameraRef) {
      const photo = await cameraRef.takePictureAsync({ skipProcessing: true });
      setPhoto(photo);
      setIsCameraMode(false);
      const response = await APIService.post(photo);
    }
  };

  if (hasPermission === null) return <View />;
  if (hasPermission === false)
    return (
      <View>
        <Text>No Access Granted To Camera</Text>
      </View>
    );
  return (
    <View style={{ flex: 1 }}>
      {isCameraMode ? (
        <Camera
          style={{ flex: 1, flexDirection: "row", justifyContent: "center" }}
          type={type}
          ref={ref => setCameraRef(ref)}
        >
          <View style={{ alignSelf: "flex-end" }}>
            <TouchableOpacity
              style={{ alignSelf: "center" }}
              onPress={takeShot}
            >
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
      ) : (
        <View
          style={{
            opacity: 0.6
          }}
        >
          <Image
            source={{ uri: photo.uri }}
            style={{
              width: "100%",
              height: "100%"
            }}
          />
        </View>
      )}
    </View>
  );
};
export default CameraView;
