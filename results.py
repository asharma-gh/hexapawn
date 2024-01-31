import pickle
from matplotlib import pyplot as plt
from model import RESULTS_FILENAME


results=[]
win_rates=[]
#
def load_results():
    global results
    try:
        results_fh=open(RESULTS_FILENAME,"rb")
        results=pickle.load(results_fh)
        results_fh.close()
    except OSError:
        print("Unable to load results file! Serialize prior to calling.")
#
def process_results():
    num_wins,num_losses=0,0
    for res in results:
        num_wins += res
        num_losses += not res
        win_rates.append(num_wins/(num_wins+num_losses))
#
def plot_results():
    X=[ii for ii in range(len(win_rates))]
    plt.plot(X,win_rates,"bo",markersize=2)
    plt.plot([0,len(win_rates)+25],[0.5,0.5],"r-",lw=1)
    plt.xlabel("Num. Games")
    plt.ylabel("AI Winrate")
    plt.show()
if __name__ == "__main__":
    load_results()
    process_results()
    plot_results()
