
# colors
# export TERM="xterm-color"
# export PS1="\e[1;30m\][\e[\e[1;30m\]\e[1;33m\] \u@\H \[\e[1;32m\]\w\[\e[0m\] \e[1;30m\]]\n[\[ \e[1;31m\]\T\[\e[0m\]\e[1;30m\] ] > \e[37m\]"
export CLICOLOR=1
export LSCOLORS=ExFxCxDxBxegedabagacad

# makes brew installed software before others
PATH=/usr/local/bin:/usr/local/sbin/:$PATH
export PATH

export CDPATH=~/work/

# work
WORKDIR=~/work
export WORKDIR

# python path
# PYTHONPATH=$PYTHONPATH:$WORKDIR/voiturolio/lib/django/
# PYTHONPATH=$PYTHONPATH:$WORKDIR/
# PYTHONPATH=$PYTHONPATH:$WORKDIR/x
# PYTHONPATH=$PYTHONPATH:$WORKDIR/x/xt
# export PYTHONPATH

# aliases
alias ll='ls -lisah'
alias s='git status'
alias d='git diff'
alias cleanpyc='find . -type f -name "*.pyc" -exec rm -f {} \;'
# alias ls='ls $LS_OPTIONS -hF'
# alias ll='ls $LS_OPTIONS -lAhF'
# alias cdwork='cd $WORKDIR'

# restaure sessions by tab for iterm2
export HISTFILE=~/.bash-history-${ITERM_SESSION_ID}


# ssh completion
_complete_ssh_hosts ()
{
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    comp_ssh_hosts=`cat ~/.ssh/config  | grep "^Host " | awk '{print $2}'`
    COMPREPLY=( $(compgen -W "${comp_ssh_hosts}" -- $cur))
    return 0
}
complete -F _complete_ssh_hosts ssh

# Bash completion 
if [ -f `brew --prefix`/etc/bash_completion ]; then
    . `brew --prefix`/etc/bash_completion
fi

# Git completion
source ~/.git-completion.bash

# nice git tips in PS1
# https://gist.github.com/921364

function git_branch {
    ref=$(git symbolic-ref HEAD 2> /dev/null) || return;
    echo "("${ref#refs/heads/}") ";
}

function git_since_last_commit {
    now=`date +%s`;
    last_commit=$(git log --pretty=format:%at -1 2> /dev/null) || return;
    seconds_since_last_commit=$((now-last_commit));
    minutes_since_last_commit=$((seconds_since_last_commit/60));
    hours_since_last_commit=$((minutes_since_last_commit/60));
    minutes_since_last_commit=$((minutes_since_last_commit%60));
                                
    echo "${hours_since_last_commit}h${minutes_since_last_commit}m ";
}

WHITE="\[\033[0m\]"
GREEN="\[\033[0;32m\]"
CYAN="\[\033[0;36m\]"
GRAY="\[\033[0;37m\]"
BLUE="\[\033[0;34m\]"
YELLOW="\[\033[0;33m\]"
# export PS1="{GREEN}\u${CYAN}@${BLUE}\h ${CYAN}\w $(__git_ps1 '(%s)') ${GRAY}$ "
GIT_PS1_SHOWDIRTYSTATE=true
GIT_PS1_SHOWUNTRACKEDFILES=true

PS1="[${GREEN}\w${WHITE}]${CYAN}\$(__git_ps1)${YELLOW} \$(git_since_last_commit)${WHITE}$ "

source ~/.django_bash_completion.bash
source ~/.VBoxManage_completion.bash
source ~/.vagrant_completion.bash


bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'
bind '"\e[C": forward-char'
bind '"\e[D": backward-char'

