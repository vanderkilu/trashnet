import "react-native-gesture-handler";
import React from "react";
import Screen from "./components/Screen";
import Dashboard from "./components/Dashboard";
import CameraView from "./components/Camera";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";

type ParamList = {
  Dashboard: undefined;
  Screen: undefined;
  CameraView: undefined;
};

const Stack = createStackNavigator<ParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Screen" component={Screen} />
        <Stack.Screen name="Dashboard" component={Dashboard} />
        <Stack.Screen name="CameraView" component={CameraView} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
