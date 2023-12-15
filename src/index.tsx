import {
  ButtonItem,
  definePlugin,
  DialogButton,
  Menu,
  MenuItem,
  PanelSection,
  PanelSectionRow,
  Router,
  ServerAPI,
  showContextMenu,
  staticClasses,
} from "decky-frontend-lib";
import { VFC, useState } from "react";
import { HiOutlineCamera } from "react-icons/hi";
import logo from "../assets/logo.png";

const Content: VFC<{ serverAPI: ServerAPI }> = ({ serverAPI }) => {
  // const [buttonEnabled, setButtonEnabled] = useState<boolean>(true);
  // const [feedbackText, setFeedbackText] = useState<string>("");

  const onClick = async () => {
      let test = serverAPI;
  };

  return (
    <PanelSection title="Panel Section">
      <PanelSectionRow>
        <ButtonItem layout="below" onClick={onClick}>Aggregate!</ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <div>test</div>
      </PanelSectionRow>
    </PanelSection>
  );
};

export default definePlugin((serverApi: ServerAPI) => {
  return {
    title: <div className={staticClasses.Title}>Screentshot Aggregator</div>,
    content: <Content serverAPI={serverApi} />,
    icon: <HiOutlineCamera />,
    onDismount() {
    },
  };
});
