from inference import InferencePipeline
import cv2

def my_sink(result, frame):
    if "output_image" in result:
        cv2.imshow("AI Park Surveillance", result["output_image"])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit(0)

pipeline = InferencePipeline.init_with_workflow(
    api_key=os.getenv("ROBOFLOW_API_KEY"),
    workspace_name="parksurveillancesystem",   # ✅ REQUIRED
    workflow_id="detect-count-and-visualize-2",
    video_reference="data/raw_videos/walking/walk1.mp4",
    max_fps=30,
    on_prediction=my_sink
)

pipeline.start()
pipeline.join()
