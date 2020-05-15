import { CameraCapturedPicture } from "expo-camera";

const BASE_URL = "http://192.168.43.156:5000/";

const APIService = {
  post(photo: CameraCapturedPicture) {
    const formData = new FormData();
    formData.append("image", {
      name: "photo.jpg",
      uri: photo.uri,
      type: "image/jpeg"
    } as any);
    return fetch(`${BASE_URL}api/image`, {
      method: "post",
      body: formData,
      headers: { "Content-Type": "multipart/form-data" }
    })
      .then(response => response.json())
      .then(response => response)
      .catch(err => console.log(err));
  }
};

export default APIService;
