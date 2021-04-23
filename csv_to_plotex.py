import pandas as pd
import sys
import math
from string import Template


def prepare_dict():
    colors = ('red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'brown', 'black')
    marks = ('', 'diamond', 'triangle', 'square')

    def is_duplicate(color, mark):
        for _, v in result.items():
            if v['color'] == color and v['mark'] == mark:
                return True
        return False
    
    color_size = len(colors)
    methods = DF['method'].unique()
    result = {m : {'color': None, 'mark': None} for m in methods}

    for i, m in enumerate(methods):
        color_idx = i % color_size
        result[m]['color'] = colors[color_idx]
        
    for m in methods:
        curr = result[m]
        for mar in marks:
            if not is_duplicate(curr['color'], m):
                curr['mark'] = mar
                break
        else:
            print('\033[91m\033[1mToo few plot markers or too many methods!!\033[0m There would be duplicate plot in each figure!', file=sys.stderr)
            sys.exit(1)

    return result


def generate_plot(method, curr_df):
    template = Template('''
            \\addplot[
                color=$color,
                mark=$mark*,
                ]
                coordinates {
                    $coords
                };
        ''')
    values = curr_df.sort_values(by='gens')[COL]
    vals = ''
    for i, v in enumerate(values, 1):
        vals += f'({i}, {v})'
    return template.substitute(**MARKS[method], coords=vals)


def generate_legend_opts(methods):
    template = Template('''
            legend entries={$methods},
            legend columns=-1,
            legend to name=named,''')
    met_str = ','.join(methods)
    return template.substitute(methods=met_str)


def generate_subfigure(width, problem, curr_df, legend=False):
    template = Template('''
    \\begin{subfigure}[b]{$width\\linewidth}
        \\resizebox{\\linewidth}{!}{%
            \\tikzset{every mark/.append style={scale=2.5}}
            \\begin{tikzpicture}
            \\begin{axis}[% $legend
            xtick={$xticks},
            xticklabels={$xticksl},
            xmin=0,
            xmax=$xmax,
            ymin=$ymin,
            ymax=$ymax,
            xlabel=\\textbf{Liczba genów},
            grid,
            grid style=dashed,
            ticklabel style={scale=1.5},
            label style={scale=1.5},
            legend style={font=\\fontsize{8}{0}\\selectfont}
            ]
            $plots
            \\end{axis}
            \\end{tikzpicture}
        }
        \\caption{$problem}
    \\end{subfigure}''')    
    problem_df = curr_df[curr_df['problem'] == problem]
    methods = problem_df['method'].unique()

    gens = problem_df['gens'].unique()
    xticklabels = ','.join(map(lambda x: f'{x}', gens))
    xmax = len(gens) + 1
    xticks = ','.join(map(lambda x: f'{x}', range(1, xmax)))
    min_, max_ = problem_df[COL].min(), problem_df[COL].max()
    padding = 0.05*(max_ - min_)
    ymin = min_ - padding
    ymax = max_ + padding
    leg = generate_legend_opts(methods) if legend else ''

    plots = ''
    for m in methods:
        plots += generate_plot(m, problem_df[problem_df['method'] == m])

    return template.substitute(legend=leg, problem=problem, plots=plots,
                               xticks=xticks, xticksl=xticklabels, xmax=xmax,
                               width=width, ymin=ymin, ymax=ymax)


def get_rows_info(problems):
    all_ = len(problems)
    if all_ > 12:
        truncated = all_ - 12
        print(f'\033[91m\033[1mToo many problems!!\033[0m This script support up to 12 problems. {truncated} problems were ignored', file=sys.stderr)
        # sys.exit(1)
    all_ = 12
    row_sizes = {
        1: 1, 2: 1, 3: 1,
        4: 1, 5: 1, 6: 2,
        7: 2, 8: 2, 9: 3,
        10: 2, 11: 3, 12: 3
    }
    row_lengths = {k: math.ceil(k/v) for k, v in row_sizes.items()}
    return row_sizes[all_], row_lengths[all_]


def generate_figure(curr_df, title, label):
    template = Template('''
\\begin{figure}[H]
 $subfigures
    \\ref{named}
    \\caption{$title}
    $label
\\end{figure}''')
    problems = curr_df['problem'].unique()
    rows, row_len = get_rows_info(problems)
    width = 1/row_len - 0.01
    width = "{:.2f}".format(width)
    subs = ''
    legend = True
    for i in range(rows):
        for p in problems[i*row_len:(i+1)*row_len]:
            subs += generate_subfigure(width, p, curr_df, legend=legend)
            legend=False
        subs += '\n'
    label_s = '\\label{' + label + '}' if label else ''
    return template.substitute(subfigures=subs, title=title, label=label_s)



    
if len(sys.argv) < 4:
    print('\033[91m\033[1mToo few arguments!!\033[0m Template of execution : \033[4m"script file.csv column_name title <label>"\033[0m <optional argument>', file=sys.stderr)
    sys.exit(1)


label = sys.argv[4] if len(sys.argv) >= 5 else None
title = sys.argv[3]

DF = pd.read_csv(sys.argv[1])
COL = sys.argv[2]
MARKS = prepare_dict()

string = generate_figure(DF, title, label)
with open('a.txt', 'w') as f:
    f.write(string)
print('\033[93mWARNING!! This script doesn\'t handle large deviations in data, so it is not guaranteed that LaTeX will compile this.\033[0m', file=sys.stderr)