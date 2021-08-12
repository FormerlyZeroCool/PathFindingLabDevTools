echo "pydots is a tool for drawing on a grid"
echo "turtle draw is a tool to show step by step"
echo "drawing of saved instructions from turtle draw"
echo
echo "Press the enter key for pydots"
echo "Type 2, then press enter for turtle_draw"
read decision
if [ $decision == "2" ]; then
  python turtle_draw.py data.txt 30
else
  python3 pydots.py
fi
